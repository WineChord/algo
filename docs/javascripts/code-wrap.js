const codeWrapStorageKey = "wc-code-wrap-v1";
let codeWrapEnabled = readCodeWrapPreference();

function readCodeWrapPreference() {
  try {
    return window.localStorage.getItem(codeWrapStorageKey) !== "off";
  } catch {
    return true;
  }
}

function writeCodeWrapPreference(enabled) {
  try {
    window.localStorage.setItem(codeWrapStorageKey, enabled ? "on" : "off");
  } catch {
    // The default wrapped layout still works when storage is unavailable.
  }
}

function updateCodeWrapButton(button) {
  const state = codeWrapEnabled ? "开" : "关";
  const action = codeWrapEnabled ? "关闭代码自动换行" : "开启代码自动换行";
  button.setAttribute("aria-pressed", String(codeWrapEnabled));
  button.setAttribute("aria-label", action);
  button.setAttribute("title", action);
  button.querySelector(".wc-code-wrap-toggle__label").textContent =
    `自动换行：${state}`;
}

function applyCodeWrapPreference() {
  document.documentElement.dataset.codeWrap = codeWrapEnabled ? "on" : "off";
  document.querySelectorAll("[data-code-wrap-toggle]").forEach(
    updateCodeWrapButton
  );
}

function createCodeWrapButton() {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "wc-code-wrap-toggle";
  button.dataset.codeWrapToggle = "";
  const label = document.createElement("span");
  label.className = "wc-code-wrap-toggle__label";
  button.append(label);
  updateCodeWrapButton(button);
  return button;
}

function codeLanguageLabel(block) {
  const languageClass = [...block.classList].find((name) =>
    name.startsWith("language-")
  );
  const language = languageClass?.slice("language-".length) || "text";
  const labels = {
    bash: "Shell",
    cpp: "C++",
    markdown: "Markdown",
    text: "文本",
  };
  return labels[language] || language.toUpperCase();
}

function enhanceCodeBlocks() {
  document.querySelectorAll("article.md-content__inner .highlight").forEach(
    (block) => {
      if (!block.querySelector(":scope > pre > code")) return;
      block.classList.add("wc-code-block");
      let toolbar = block.querySelector(":scope > .wc-code-toolbar");
      if (!toolbar) {
        toolbar = document.createElement("div");
        toolbar.className = "wc-code-toolbar";
        toolbar.setAttribute("role", "toolbar");
        toolbar.setAttribute("aria-label", "代码显示设置");
        block.prepend(toolbar);
      }
      let language = toolbar.querySelector(":scope > .wc-code-language");
      if (!language) {
        language = document.createElement("span");
        language.className = "wc-code-language";
        toolbar.prepend(language);
      }
      language.textContent = codeLanguageLabel(block);
      let button = toolbar.querySelector(":scope > [data-code-wrap-toggle]");
      if (!button) {
        button = createCodeWrapButton();
        toolbar.append(button);
      }
      const codeNavigation = block.querySelector(
        ":scope > pre > .md-code__nav"
      );
      if (codeNavigation) toolbar.insertBefore(codeNavigation, button);
      const clipboard = block.querySelector(":scope > .md-clipboard");
      if (clipboard) toolbar.insertBefore(clipboard, button);
    }
  );
  applyCodeWrapPreference();
}

function setCodeWrapPreference(enabled) {
  codeWrapEnabled = enabled;
  writeCodeWrapPreference(enabled);
  applyCodeWrapPreference();
}

document.addEventListener("click", (event) => {
  const button = event.target.closest?.("[data-code-wrap-toggle]");
  if (!button) return;
  event.preventDefault();
  setCodeWrapPreference(!codeWrapEnabled);
});

window.addEventListener("storage", (event) => {
  if (event.key !== codeWrapStorageKey) return;
  codeWrapEnabled = event.newValue !== "off";
  applyCodeWrapPreference();
});

window.addEventListener("DOMContentLoaded", enhanceCodeBlocks);
if (typeof document$ !== "undefined") {
  document$.subscribe(() => requestAnimationFrame(enhanceCodeBlocks));
}
enhanceCodeBlocks();
