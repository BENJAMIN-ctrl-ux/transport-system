// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {
  // Sidebar toggle for mobile
  const sidebarToggle = document.getElementById("sidebar-toggle");
  const sidebar = document.getElementById("sidebar");

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("hidden");
    });
  }

  // Modal triggers
  const modalTriggers = document.querySelectorAll("[data-modal-trigger]");
  const modals = document.querySelectorAll("[data-modal]");
  const modalCloses = document.querySelectorAll("[data-modal-close]");

  modalTriggers.forEach(trigger => {
    const target = trigger.getAttribute("data-modal-trigger");
    trigger.addEventListener("click", () => {
      document.querySelector(`[data-modal="${target}"]`).classList.remove("hidden");
    });
  });

  modalCloses.forEach(btn => {
    btn.addEventListener("click", () => {
      btn.closest("[data-modal]").classList.add("hidden");
    });
  });

  // Toast notifications (optional setup)
  const toast = document.getElementById("toast");
  if (toast) {
    setTimeout(() => {
      toast.classList.add("opacity-0");
    }, 3000);
  }
});
