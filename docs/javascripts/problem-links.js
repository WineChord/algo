function openLinkedProblem() {
  const id = decodeURIComponent(window.location.hash.slice(1));
  if (!id.startsWith("problem-")) return;
  const anchor = document.getElementById(id);
  const details = anchor?.nextElementSibling;
  if (!(details instanceof HTMLDetailsElement) || !details.classList.contains("problem")) return;
  details.open = true;
  requestAnimationFrame(() => anchor.scrollIntoView({ block: "start" }));
}
window.addEventListener("DOMContentLoaded", openLinkedProblem);
window.addEventListener("hashchange", openLinkedProblem);
globalThis.document$?.subscribe(openLinkedProblem);
