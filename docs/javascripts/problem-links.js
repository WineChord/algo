let pendingProblemId = null;
function problemIdFromHash(hash) {
  try {
    const id = decodeURIComponent(hash.replace(/^#/, ""));
    return id.startsWith("problem-") ? id : null;
  } catch {
    return null;
  }
}
function rememberLinkedProblem(event) {
  const link = event.target.closest?.('a[href*="#problem-"]');
  if (!link) return;
  pendingProblemId = problemIdFromHash(new URL(link.href, window.location.href).hash);
}
function openLinkedProblem() {
  const id = problemIdFromHash(window.location.hash) || pendingProblemId;
  if (!id) return;
  const anchor = document.getElementById(id);
  if (!anchor) {
    pendingProblemId = id;
    return;
  }
  const details = anchor?.nextElementSibling;
  if (!(details instanceof HTMLDetailsElement) || !details.classList.contains("problem")) return;
  details.open = true;
  pendingProblemId = null;
  history.replaceState(history.state, "", `#${encodeURIComponent(id)}`);
  requestAnimationFrame(() => anchor.scrollIntoView({ block: "start" }));
}
pendingProblemId = problemIdFromHash(window.location.hash);
document.addEventListener("click", rememberLinkedProblem, true);
window.addEventListener("DOMContentLoaded", openLinkedProblem);
window.addEventListener("hashchange", openLinkedProblem);
if (typeof document$ !== "undefined") document$.subscribe(openLinkedProblem);
openLinkedProblem();
