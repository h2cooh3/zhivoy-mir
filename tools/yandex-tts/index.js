// Облачная функция Yandex Cloud: посредник между приложением «Живой мир» и Yandex SpeechKit (синтез речи, API v3).
// Среда выполнения: Node.js 18+ (nodejs18 / nodejs22). Точка входа: index.handler
// Переменные окружения: FOLDER_ID — ID каталога; SECRET — любое слово-пароль (то же вписываешь в приложении).
// Функции нужен сервисный аккаунт с ролью ai.speechkit-tts.user — тогда ключ в приложение класть не нужно.
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST,OPTIONS",
};
module.exports.handler = async (event, context) => {
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers: CORS, body: "" };
  let body = {};
  try {
    const raw = event.isBase64Encoded ? Buffer.from(event.body || "", "base64").toString() : (event.body || "{}");
    body = JSON.parse(raw);
  } catch (e) { return { statusCode: 400, headers: CORS, body: "bad json" }; }
  if (process.env.SECRET && body.secret !== process.env.SECRET) return { statusCode: 403, headers: CORS, body: "wrong secret" };
  const text = String(body.text || "").slice(0, 1000);
  if (!text.trim()) return { statusCode: 400, headers: CORS, body: "empty text" };
  const token = context && context.token && context.token.access_token;
  if (!token) return { statusCode: 500, headers: CORS, body: "no service account: attach one with role ai.speechkit-tts.user" };
  const hints = [{ voice: String(body.voice || "alena") }];
  if (body.role) hints.push({ role: String(body.role) });
  if (body.speed) hints.push({ speed: Number(body.speed) });
  const r = await fetch("https://tts.api.cloud.yandex.net/tts/v3/utteranceSynthesis", {
    method: "POST",
    headers: { "Authorization": "Bearer " + token, "x-folder-id": process.env.FOLDER_ID || "", "content-type": "application/json" },
    body: JSON.stringify({ text, hints, outputAudioSpec: { containerAudio: { containerAudioType: "MP3" } }, loudnessNormalizationType: "LUFS" }),
  });
  const out = await r.text();
  if (!r.ok) return { statusCode: r.status, headers: CORS, body: out.slice(0, 500) };
  // ответ — строки JSON, в каждой кусок аудио base64
  const parts = [];
  for (const line of out.split("\n")) {
    if (!line.trim()) continue;
    try { const j = JSON.parse(line); const d = j.result && j.result.audioChunk && j.result.audioChunk.data; if (d) parts.push(Buffer.from(d, "base64")); } catch (e) {}
  }
  if (!parts.length) return { statusCode: 502, headers: CORS, body: "no audio: " + out.slice(0, 300) };
  return { statusCode: 200, headers: { ...CORS, "content-type": "audio/mpeg" }, isBase64Encoded: true, body: Buffer.concat(parts).toString("base64") };
};
