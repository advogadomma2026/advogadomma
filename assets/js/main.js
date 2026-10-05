/* Advocacia e Consultoria Jurídica MMA — interações do site */
(function () {
  "use strict";

  var WA = "https://wa.me/5571997260142";

  /* ---------------------------------------------------- header ao rolar */
  var header = document.getElementById("siteHeader");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* -------------------------------------------------------- menu mobile */
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("mainNav");
  var backdrop = document.getElementById("navBackdrop");

  function setMenu(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    document.body.style.overflow = open ? "hidden" : "";
    if (backdrop) backdrop.hidden = !open;
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(!nav.classList.contains("is-open"));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    if (backdrop) backdrop.addEventListener("click", function () { setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 940) setMenu(false);
    });
  }

  /* -------------------------------------------- links internos / âncoras */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (!id || id === "#") return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.scrollY;
      var offset = (header ? header.offsetHeight : 72) + 12;
      window.scrollTo({
        top: id === "#inicio" ? 0 : Math.max(0, top - offset),
        behavior: "smooth"
      });
      history.replaceState(null, "", id);
    });
  });

  /* ------------------------------------------------- animação ao rolar */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length) {
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            var siblings = Array.prototype.slice.call(el.parentElement.children);
            var i = siblings.indexOf(el);
            el.style.transitionDelay = Math.min(i < 0 ? 0 : i, 6) * 70 + "ms";
            el.classList.add("is-visible");
            io.unobserve(el);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add("is-visible"); });
    }
  }

  /* ------------------------------------------------------- ano no rodapé */
  /* (o ano é gerado no build, nada a fazer aqui) */

  /* ------------------------------------------------- formulário -> Zap */
  var form = document.getElementById("contactForm");
  var status = document.getElementById("formStatus");
  if (form && status) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form__status";
      status.textContent = "";

      var data = new FormData(form);
      var nome = (data.get("nome") || "").toString().trim();
      var fone = (data.get("telefone") || "").toString().trim();
      var email = (data.get("email") || "").toString().trim();
      var area = (data.get("area") || "").toString().trim();
      var msg = (data.get("mensagem") || "").toString().trim();

      var invalidos = form.querySelectorAll(".is-invalid");
      invalidos.forEach(function (el) { el.classList.remove("is-invalid"); });

      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
      var problemas = [];
      if (nome.length < 2) problemas.push("nome");
      if (fone.replace(/\D/g, "").length < 8) problemas.push("telefone");
      if (!emailOk) problemas.push("e-mail");
      if (msg.length < 10) problemas.push("descrição do caso");

      if (problemas.length) {
        problemas.forEach(function (p) {
          var input = form.querySelector('[name="' + (p === "descrição do caso" ? "mensagem" : p) + '"]');
          if (input) input.classList.add("is-invalid");
        });
        status.className = "form__status is-err";
        status.textContent = "Confira os campos destacados antes de enviar.";
        var first = form.querySelector(".is-invalid");
        if (first) first.focus();
        return;
      }

      var texto =
        "Olá! Vim pelo site da Advocacia e Consultoria Jurídica MMA.\n\n" +
        "Nome: " + nome + "\n" +
        "Telefone: " + fone + "\n" +
        "E-mail: " + email + "\n" +
        "Área do Direito: " + (area || "Não informado") + "\n\n" +
        "Descrição do caso:\n" + msg;

      var url = WA + "?text=" + encodeURIComponent(texto);
      status.className = "form__status is-ok";
      status.textContent = "Abrindo o WhatsApp com a sua mensagem…";
      window.open(url, "_blank", "noopener");
      form.reset();
    });
  }

  /* --------------------------------------------- marcação do item ativo */
  var sections = ["areas", "sobre", "servicos", "faq", "contato"]
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  if (sections.length && "IntersectionObserver" in window) {
    var links = {};
    document.querySelectorAll(".nav__link").forEach(function (l) {
      var h = l.getAttribute("href");
      if (h && h.charAt(0) === "#") links[h.slice(1)] = l;
    });

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = links[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].classList.remove("is-active"); });
          link.classList.add("is-active");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    sections.forEach(function (s) { spy.observe(s); });
  }
})();