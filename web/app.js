/* MiniMax Music 3 · 巴洛克音乐工房 · 前端逻辑 */

const $ = (id) => document.getElementById(id);

const els = {
  structure: $("structure"), tagRow: $("tagRow"), lyrics: $("lyrics"),
  preset: $("preset"), genre: $("genre"), subgenre: $("subgenre"),
  bpm: $("bpm"), bpmVal: $("bpmVal"), bpmAuto: $("bpmAuto"),
  key: $("key"), scale: $("scale"),
  emotionalArc: $("emotionalArc"), scenario: $("scenario"), production: $("production"),
  vocalGender: $("vocalGender"), timbre: $("timbre"), register: $("register"),
  delivery: $("delivery"), harmony: $("harmony"), backingVocals: $("backingVocals"), vocalEffect: $("vocalEffect"),
  primaryInstruments: $("primaryInstruments"), secondaryInstruments: $("secondaryInstruments"),
  groove: $("groove"), bass: $("bass"), percussion: $("percussion"), spatial: $("spatial"),
  textures: $("textures"), arrangementNotes: $("arrangementNotes"),
  audioDuration: $("audioDuration"), durVal: $("durVal"),
  numInferenceSteps: $("numInferenceSteps"), stepsVal: $("stepsVal"),
  seed: $("seed"), vramMode: $("vramMode"),
  previewBtn: $("previewBtn"), captionPreview: $("captionPreview"),
  saveBtn: $("saveBtn"), loadBtn: $("loadBtn"), configFile: $("configFile"),
  generateBtn: $("generateBtn"),
  forgeProgress: $("forgeProgress"), progressMsg: $("progressMsg"),
  progressFill: $("progressFill"), forgeLog: $("forgeLog"),
  player: $("player"), resultMeta: $("resultMeta"),
  archive: $("archive"), outputsCount: $("outputsCount"),
  simpleField: $("simpleField"), simplePrompt: $("simplePrompt"), structuredBody: $("structuredBody"),
  primaryCount: $("primaryCount"), secondaryCount: $("secondaryCount"),
};

const TAG_TIPS = {
  "[Intro]": {
    zh: "前奏",
    what: "开场器乐段落,先行铺设情绪与和声底色,随后人声进入。",
    where: "放在歌词最顶部、第一段主歌之前。",
  },
  "[Verse]": {
    zh: "主歌",
    what: "叙事主体段落,逐段推进故事与细节,旋律平稳亲和。",
    where: "放在前奏、导歌或上一遍副歌之后,可反复出现。",
  },
  "[Pre-Chorus]": {
    zh: "导歌",
    what: "主歌通往副歌的过渡段,情绪逐句抬升,为副歌蓄力。",
    where: "放在主歌之后、副歌之前。",
  },
  "[Chorus]": {
    zh: "副歌",
    what: "全曲情绪与记忆的顶点,歌名与主题句通常落在这里。",
    where: "放在导歌或主歌之后,整首歌曲通常重复多遍。",
  },
  "[Post-Chorus]": {
    zh: "副歌后段",
    what: "副歌收束后的短小钩子,延续余韵,常伴随节奏型插部。",
    where: "放在每遍副歌之后、下一段主歌之前。",
  },
  "[Bridge]": {
    zh: "桥段",
    what: "打破循环的对比段,常引入新旋律、转调或新配器。",
    where: "放在第二遍副歌之后、最后一遍副歌之前。",
  },
  "[Instrumental]": {
    zh: "器乐段",
    what: "纯伴奏演奏段落,无人声演唱,给歌曲留出呼吸空间。",
    where: "可插在任意两段人声之间,或紧随前奏。",
  },
  "[Solo]": {
    zh: "独奏",
    what: "单件乐器的炫技段落,电吉他与键盘最为常见。",
    where: "放在歌曲后半程,两遍副歌之间。",
  },
  "[Outro]": {
    zh: "尾奏",
    what: "全曲的收束段落,或渐弱淡出,或利落终止。",
    where: "放在歌词最末一行之后。",
  },
};

const DEFAULT_LYRICS = `[Verse]
晨光穿过高高的白杨
风把昨夜的梦轻轻晾干
[Pre-Chorus]
我数着心跳靠近答案
[Chorus]
把热爱唱成漫天星光
每一步都朝着远方`;

const NONE = "(不指定)";
let CONFIG = null;
let mode = "结构化参数";

/* ── 选项填充 ── */

function fillSelect(sel, options, value) {
  sel.innerHTML = "";
  for (const opt of options) {
    const o = document.createElement("option");
    o.value = opt; o.textContent = opt;
    sel.appendChild(o);
  }
  if (value !== undefined) sel.value = value;
}

const keys = (obj) => Object.keys(obj);

function populate() {
  const c = CONFIG;
  fillSelect(els.structure, ["(请选择…)"].concat(keys(c.song_structures)));
  fillSelect(els.preset, ["(请选择…)"].concat(keys(c.style_presets)));
  fillSelect(els.genre, keys(c.genres));
  fillSelect(els.key, ["(自动)"].concat(c.keys));
  fillSelect(els.scale, ["(自动)"].concat(keys(c.scales)));
  fillSelect(els.emotionalArc, [NONE].concat(keys(c.emotional_arcs)));
  fillSelect(els.scenario, [NONE].concat(keys(c.scenarios)));
  fillSelect(els.production, [NONE].concat(keys(c.production_profiles)));
  fillSelect(els.vocalGender, keys(c.vocal_genders), "女声");
  fillSelect(els.timbre, [NONE].concat(keys(c.vocal_timbres)));
  fillSelect(els.register, [NONE].concat(keys(c.vocal_registers)));
  fillSelect(els.delivery, [NONE].concat(keys(c.vocal_deliveries)));
  fillSelect(els.harmony, keys(c.harmonies));
  fillSelect(els.backingVocals, keys(c.backing_vocals));
  fillSelect(els.vocalEffect, keys(c.vocal_effects));
  fillSelect(els.groove, [NONE].concat(keys(c.grooves)));
  const bassKeys = keys(c.instruments).filter((k) => k.includes("贝斯") || k.toLowerCase().includes("bass"));
  fillSelect(els.bass, ["(跟随主乐器自动)"].concat(bassKeys));
  fillSelect(els.percussion, [NONE].concat(keys(c.percussion_styles)));
  fillSelect(els.spatial, [NONE].concat(keys(c.spatial_effects)));

  buildChecks(els.primaryInstruments, keys(c.instruments));
  buildChecks(els.secondaryInstruments, keys(c.instruments));
  buildChecks(els.textures, keys(c.textures));

  for (const tag of c.section_tags) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "tag-btn";
    const txt = document.createElement("span");
    txt.className = "tag-txt"; txt.textContent = tag;
    b.appendChild(txt);
    const tip = TAG_TIPS[tag];
    if (tip) {
      const tipEl = document.createElement("span");
      tipEl.className = "tag-tip";
      tipEl.setAttribute("role", "tooltip");
      const nm = document.createElement("span");
      nm.className = "tt-name"; nm.textContent = `${tip.zh} ${tag}`;
      const wh = document.createElement("span");
      wh.className = "tt-what"; wh.textContent = tip.what;
      const we = document.createElement("span");
      we.className = "tt-where";
      const ico = document.createElement("img");
      ico.src = "/static/assets/note-burgundy.svg"; ico.alt = "";
      const weTxt = document.createElement("span");
      weTxt.textContent = tip.where;
      we.append(ico, weTxt);
      tipEl.append(nm, wh, we);
      b.appendChild(tipEl);
      b.setAttribute("aria-label", `${tag}(${tip.zh}):${tip.what}${tip.where}`);
    }
    b.addEventListener("click", () => insertTag(tag));
    els.tagRow.appendChild(b);
  }

  els.lyrics.value = DEFAULT_LYRICS;
}

function buildChecks(container, items) {
  container.innerHTML = "";
  for (const item of items) {
    const label = document.createElement("label");
    label.className = "check-item";
    const cb = document.createElement("input");
    cb.type = "checkbox"; cb.value = item;
    const span = document.createElement("span");
    span.textContent = item;
    label.append(cb, span);
    container.appendChild(label);
  }
  container.addEventListener("change", () => updateCounts());
}

function checkedValues(container) {
  return Array.from(container.querySelectorAll("input:checked")).map((i) => i.value);
}

function setChecks(container, values) {
  for (const cb of container.querySelectorAll("input")) {
    cb.checked = values.includes(cb.value);
  }
}

function updateCounts() {
  const p = checkedValues(els.primaryInstruments).length;
  const s = checkedValues(els.secondaryInstruments).length;
  els.primaryCount.textContent = p ? `已选 ${p} 件` : "未选";
  els.secondaryCount.textContent = s ? `已选 ${s} 件` : "未选";
}

/* ── 歌词标签插入 ── */

function insertTag(tag) {
  const ta = els.lyrics;
  const start = ta.selectionStart, end = ta.selectionEnd;
  const before = ta.value.slice(0, start);
  const after = ta.value.slice(end);
  const lead = before && !before.endsWith("\n") ? "\n" : "";
  ta.value = before + lead + tag + "\n" + after.replace(/^\n+/, "");
  ta.focus();
  const pos = (before + lead + tag + "\n").length;
  ta.setSelectionRange(pos, pos);
}

/* ── 模式切换 ── */

document.querySelectorAll(".mode-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    mode = btn.dataset.mode;
    document.querySelectorAll(".mode-btn").forEach((b) => b.classList.toggle("active", b === btn));
    const simple = mode === "简单描述";
    els.simpleField.hidden = !simple;
    els.structuredBody.style.display = simple ? "none" : "";
  });
});

/* ── 滑杆联动 ── */

function bindRange(el, out, fmt) {
  const sync = () => {
    const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
    el.style.setProperty("--fill", pct + "%");
    out.textContent = fmt ? fmt(el.value) : el.value;
  };
  el.addEventListener("input", sync);
  sync();
}
bindRange(els.bpm, els.bpmVal);
bindRange(els.audioDuration, els.durVal, (v) => `${v} 秒`);
bindRange(els.numInferenceSteps, els.stepsVal);
els.bpmAuto.addEventListener("change", () => { els.bpm.disabled = els.bpmAuto.checked; });

/* ── 预设应用 ── */

els.preset.addEventListener("change", () => {
  const p = CONFIG.style_presets[els.preset.value];
  if (!p) return;
  if (p.genre !== undefined) els.genre.value = p.genre;
  els.subgenre.value = p.subgenre || "";
  els.bpmAuto.checked = false; els.bpm.disabled = false;
  els.bpm.value = p.bpm || 100; els.bpm.dispatchEvent(new Event("input"));
  els.key.value = p.key || "(自动)";
  els.scale.value = p.scale || "(自动)";
  els.emotionalArc.value = p.arc && keys(CONFIG.emotional_arcs).includes(p.arc) ? p.arc : NONE;
  els.scenario.value = NONE;
  els.production.value = p.production && keys(CONFIG.production_profiles).includes(p.production) ? p.production : NONE;
  els.vocalGender.value = p.vocal_gender || "女声";
  els.timbre.value = p.timbre && keys(CONFIG.vocal_timbres).includes(p.timbre) ? p.timbre : NONE;
  els.register.value = p.register && keys(CONFIG.vocal_registers).includes(p.register) ? p.register : NONE;
  els.delivery.value = p.delivery && keys(CONFIG.vocal_deliveries).includes(p.delivery) ? p.delivery : NONE;
  els.harmony.value = p.harmony && keys(CONFIG.harmonies).includes(p.harmony) ? p.harmony : "无和声";
  els.backingVocals.value = p.backing_vocals && keys(CONFIG.backing_vocals).includes(p.backing_vocals) ? p.backing_vocals : "无伴唱";
  els.vocalEffect.value = "无效果";
  setChecks(els.primaryInstruments, p.primary || []);
  setChecks(els.secondaryInstruments, p.secondary || []);
  els.groove.value = p.groove && keys(CONFIG.grooves).includes(p.groove) ? p.groove : NONE;
  els.bass.value = "(跟随主乐器自动)";
  els.percussion.value = p.percussion && keys(CONFIG.percussion_styles).includes(p.percussion) ? p.percussion : NONE;
  setChecks(els.textures, p.texture || []);
  els.spatial.value = p.spatial && keys(CONFIG.spatial_effects).includes(p.spatial) ? p.spatial : NONE;
  updateCounts();
});

els.structure.addEventListener("change", () => {
  const text = CONFIG.song_structures[els.structure.value];
  if (!text) return;
  els.lyrics.value = text;
});

/* ── 参数收集 ── */

function payload() {
  return {
    prompt_mode: mode,
    simple_prompt: els.simplePrompt.value.trim(),
    genre: els.genre.value,
    subgenre: els.subgenre.value.trim(),
    bpm_auto: els.bpmAuto.checked,
    bpm: Number(els.bpm.value),
    key: els.key.value,
    scale: els.scale.value,
    emotional_arc: els.emotionalArc.value,
    scenario: els.scenario.value,
    production: els.production.value,
    vocal_gender: els.vocalGender.value,
    timbre: els.timbre.value,
    register: els.register.value,
    delivery: els.delivery.value,
    harmony: els.harmony.value,
    backing_vocals: els.backingVocals.value,
    vocal_effect: els.vocalEffect.value,
    primary_instruments: checkedValues(els.primaryInstruments),
    secondary_instruments: checkedValues(els.secondaryInstruments),
    groove: els.groove.value,
    bass: els.bass.value,
    percussion: els.percussion.value,
    textures: checkedValues(els.textures),
    spatial: els.spatial.value,
    arrangement_notes: els.arrangementNotes.value.trim(),
    lyrics: els.lyrics.value,
    audio_duration: Number(els.audioDuration.value),
    num_inference_steps: Number(els.numInferenceSteps.value),
    seed: Number(els.seed.value || -1),
    vram_mode: els.vramMode.value,
  };
}

/* ── Caption 预览 ── */

els.previewBtn.addEventListener("click", async () => {
  els.captionPreview.value = "正在生成预览……";
  try {
    const res = await fetch("/api/caption", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload()),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    const caption = data.caption || "(提示词为空:请填写自由描述,或切换到参数模式选择)";
    const lyrics = (data.lyrics || "").trim();
    els.captionPreview.value = lyrics
      ? `—— 音乐描述(送入 prompt)——\n${caption}\n\n—— 歌词(送入 lyrics)——\n${lyrics}`
      : caption + "\n\n(歌词为空:请在左侧填写歌词,纯器乐也需要段落标签)";
  } catch (e) {
    els.captionPreview.value = "预览失败: " + e.message;
  }
});

/* ── 配置保存与导入 ── */

const CONFIG_SCHEMA = 1;

els.saveBtn.addEventListener("click", () => {
  const data = {
    app: "minimax-music3-workspace-zhCN",
    schema: CONFIG_SCHEMA,
    saved_at: new Date().toISOString(),
    params: payload(),
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const ts = new Date().toISOString().slice(0, 16).replace(/[T:]/g, "-");
  const a = document.createElement("a");
  a.href = url;
  a.download = `music-config-${ts}.json`;
  a.click();
  URL.revokeObjectURL(url);
  log(`配置已导出:歌词 ${data.params.lyrics.length} 字符`);
});

els.loadBtn.addEventListener("click", () => els.configFile.click());

els.configFile.addEventListener("change", () => {
  const file = els.configFile.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      const params = data && data.params ? data.params : data;
      if (!params || typeof params !== "object") throw new Error("缺少 params 对象");
      applyParams(params);
      log(`配置已导入:${file.name}`);
    } catch (e) {
      alert("导入失败:" + e.message);
    } finally {
      els.configFile.value = "";
    }
  };
  reader.onerror = () => {
    alert("读取文件失败");
    els.configFile.value = "";
  };
  reader.readAsText(file, "utf-8");
});

function setSel(el, value) {
  if (value === undefined || value === null) return;
  const hit = Array.from(el.options).some((o) => o.value === value);
  if (hit) el.value = value;
  else if (value !== "(不指定)") log(`「${el.id}」的选项「${value}」在当前选项库中不存在,已保留原值`);
}

function applyParams(p) {
  const wantMode = p.prompt_mode === "简单描述" ? "简单描述" : "结构化参数";
  const btn = document.querySelector(`.mode-btn[data-mode="${wantMode}"]`);
  if (btn) btn.click();

  els.simplePrompt.value = p.simple_prompt || "";
  setSel(els.genre, p.genre);
  els.subgenre.value = p.subgenre || "";
  els.bpmAuto.checked = !!p.bpm_auto;
  els.bpm.disabled = els.bpmAuto.checked;
  if (p.bpm !== undefined) { els.bpm.value = p.bpm; els.bpm.dispatchEvent(new Event("input")); }
  setSel(els.key, p.key);
  setSel(els.scale, p.scale);
  setSel(els.emotionalArc, p.emotional_arc);
  setSel(els.scenario, p.scenario);
  setSel(els.production, p.production);
  setSel(els.vocalGender, p.vocal_gender);
  setSel(els.timbre, p.timbre);
  setSel(els.register, p.register);
  setSel(els.delivery, p.delivery);
  setSel(els.harmony, p.harmony);
  setSel(els.backingVocals, p.backing_vocals);
  setSel(els.vocalEffect, p.vocal_effect);
  setChecks(els.primaryInstruments, p.primary_instruments || []);
  setChecks(els.secondaryInstruments, p.secondary_instruments || []);
  setSel(els.groove, p.groove);
  setSel(els.bass, p.bass);
  setSel(els.percussion, p.percussion);
  setChecks(els.textures, p.textures || []);
  setSel(els.spatial, p.spatial);
  els.arrangementNotes.value = p.arrangement_notes || "";
  els.lyrics.value = p.lyrics !== undefined ? p.lyrics : els.lyrics.value;
  if (p.audio_duration !== undefined) { els.audioDuration.value = p.audio_duration; els.audioDuration.dispatchEvent(new Event("input")); }
  if (p.num_inference_steps !== undefined) { els.numInferenceSteps.value = p.num_inference_steps; els.numInferenceSteps.dispatchEvent(new Event("input")); }
  if (p.seed !== undefined) els.seed.value = p.seed;
  if (p.vram_mode !== undefined) els.vramMode.value = p.vram_mode;
  updateCounts();
}

/* ── 生成(SSE) ── */

function log(line) {
  els.forgeLog.textContent += `[${new Date().toLocaleTimeString("zh-CN", { hour12: false })}] ${line}\n`;
  els.forgeLog.scrollTop = els.forgeLog.scrollHeight;
}

els.generateBtn.addEventListener("click", async () => {
  els.generateBtn.disabled = true;
  els.forgeProgress.hidden = false;
  els.forgeLog.textContent = "";
  els.progressFill.style.width = "0%";
  els.progressMsg.textContent = "准备中";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload()),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "HTTP " + res.status }));
      throw new Error(err.detail || "HTTP " + res.status);
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf("\n\n")) >= 0) {
        const chunk = buf.slice(0, idx).trim();
        buf = buf.slice(idx + 2);
        if (!chunk.startsWith("data:")) continue;
        const ev = JSON.parse(chunk.slice(5).trim());
        handleEvent(ev);
        if (ev.type === "result" || ev.type === "error") return finish();
      }
    }
    finish();
  } catch (e) {
    log("失败: " + e.message);
    els.progressMsg.textContent = "中断";
    finish();
  }

  function finish() {
    els.generateBtn.disabled = false;
    loadArchive();
  }
});

function handleEvent(ev) {
  if (ev.type === "progress") {
    els.progressFill.style.width = Math.round(ev.frac * 100) + "%";
    els.progressMsg.textContent = ev.message;
    log(ev.message);
  } else if (ev.type === "log") {
    log(ev.message);
  } else if (ev.type === "result") {
    els.progressFill.style.width = "100%";
    els.progressMsg.textContent = "生成完成";
    log(`完成:采样率 ${ev.sample_rate} Hz,时长 ${ev.duration} 秒,seed=${ev.seed}`);
    els.player.src = ev.url;
    els.player.play().catch(() => {});
    els.resultMeta.textContent = `采样率 ${ev.sample_rate} Hz · 时长 ${ev.duration} 秒 · seed ${ev.seed} · ${ev.file}`;
  } else if (ev.type === "error") {
    els.progressMsg.textContent = "出错";
    log("错误: " + ev.message);
  }
}

/* ── 曲库 ── */

const NOTE_SVG = '<img class="note-ico" src="/static/assets/note-gold.svg" alt="">';

async function loadArchive() {
  try {
    const res = await fetch("/api/outputs");
    const items = await res.json();
    els.archive.innerHTML = "";
    els.outputsCount.textContent = items.length ? `共 ${items.length} 首` : "";
    if (!items.length) {
      const li = document.createElement("li");
      li.className = "empty";
      li.textContent = "暂无历史作品,生成后自动保存到这里。";
      els.archive.appendChild(li);
      return;
    }
    for (const item of items) {
      const li = document.createElement("li");
      li.dataset.url = item.url;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.innerHTML = `${NOTE_SVG}<span class="fname"></span><span class="fmeta">${item.size_mb} MB · ${item.mtime.slice(5, 16)}</span>`;
      btn.querySelector(".fname").textContent = item.file;
      btn.addEventListener("click", () => {
        els.player.src = item.url;
        els.player.play().catch(() => {});
        els.resultMeta.textContent = `正在播放 ${item.file}`;
        els.archive.querySelectorAll("li").forEach((x) => x.classList.remove("playing"));
        li.classList.add("playing");
      });
      li.appendChild(btn);
      els.archive.appendChild(li);
    }
  } catch (e) {
    els.outputsCount.textContent = "";
  }
}

/* ── 启动 ── */

(async function init() {
  try {
    const res = await fetch("/api/config");
    CONFIG = await res.json();
    populate();
    updateCounts();
    await loadArchive();
  } catch (e) {
    document.querySelector(".epigraph").textContent = "无法连接后端服务(" + e.message + "),请确认服务已启动。";
  }
})();
