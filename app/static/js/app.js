const $ = (id) => document.getElementById(id);
$("host").textContent = location.host + "/";

function setMsg(text, isErr) {
  $("msg").textContent = text;
  $("msg").className = isErr ? "err" : "";
}

async function copyText(text, btn) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    return setMsg("Gagal menyalin. Salin manual dari kotak link.", true);
  }
  const old = btn.textContent;
  btn.textContent = "Tersalin";
  setTimeout(() => (btn.textContent = old), 1500);
}

async function loadList() {
  const res = await fetch("/api/links");
  const items = await res.json();
  const ul = $("list");
  ul.replaceChildren();
  if (!items.length) {
    const li = document.createElement("li");
    li.className = "empty";
    li.textContent = "Belum ada link. Buat yang pertama di atas.";
    ul.append(li);
    return;
  }
  for (const it of items) {
    const li = document.createElement("li");
    const row = document.createElement("div");
    row.className = "row";

    const a = document.createElement("a");
    a.className = "short";
    a.href = it.short_url;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = it.short_url;

    const actions = document.createElement("div");
    actions.className = "actions";
    const cp = document.createElement("button");
    cp.className = "ghost";
    cp.textContent = "Salin";
    cp.onclick = () => copyText(it.short_url, cp);
    const del = document.createElement("button");
    del.className = "ghost danger";
    del.textContent = "Hapus";
    del.onclick = async () => {
      if (!confirm("Hapus link " + it.code + "?")) return;
      await fetch("/api/links/" + encodeURIComponent(it.code), { method: "DELETE" });
      loadList();
    };
    actions.append(cp, del);
    row.append(a, actions);

    const orig = document.createElement("div");
    orig.className = "orig";
    orig.textContent = it.url;
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = it.clicks + " klik · dibuat " + it.created_at + " UTC";

    li.append(row, orig, meta);
    ul.append(li);
  }
}

$("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  setMsg("");
  $("result").classList.remove("show");
  $("go").disabled = true;
  try {
    const res = await fetch("/api/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: $("url").value, alias: $("alias").value }),
    });
    const data = await res.json();
    if (!res.ok) return setMsg(data.error || "Terjadi kesalahan.", true);
    $("out").href = data.short_url;
    $("out").textContent = data.short_url;
    $("result").classList.add("show");
    $("copy").onclick = () => copyText(data.short_url, $("copy"));
    $("url").value = "";
    $("alias").value = "";
    loadList();
  } catch {
    setMsg("Tidak bisa terhubung ke server.", true);
  } finally {
    $("go").disabled = false;
  }
});

loadList();
