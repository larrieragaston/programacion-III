;(function () {
  if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
    document.querySelectorAll('a[data-dev-port]').forEach(function (link) {
      var port = link.dataset.devPort
      var path = link.dataset.devPath
      var base = 'http://localhost:' + port
      if (path) {
        if (path.charAt(0) !== '/') path = '/' + path
        link.href = base + path
      } else {
        link.href = base + '/'
      }
    })
  }

  function closeAllDownloadMenus() {
    document.querySelectorAll('.card-download-menu.is-open').forEach(function (root) {
      root.classList.remove('is-open')
      var panel = root.querySelector('.card-download-menu-panel')
      var trigger = root.querySelector('.card-download-menu-trigger')
      if (panel) panel.hidden = true
      if (trigger) trigger.setAttribute('aria-expanded', 'false')
    })
  }

  document.querySelectorAll('.card-download-menu').forEach(function (root) {
    var trigger = root.querySelector('.card-download-menu-trigger')
    var panel = root.querySelector('.card-download-menu-panel')
    if (!trigger || !panel) return

    trigger.addEventListener('click', function (e) {
      e.stopPropagation()
      if (root.classList.contains('is-disabled')) return
      var willOpen = panel.hidden
      closeAllDownloadMenus()
      if (willOpen) {
        root.classList.add('is-open')
        panel.hidden = false
        trigger.setAttribute('aria-expanded', 'true')
      }
    })

    panel.addEventListener('click', function (e) {
      if (e.target.closest('a[href]') && !e.target.closest('a.is-disabled')) closeAllDownloadMenus()
    })
  })

  document.addEventListener('click', closeAllDownloadMenus)

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllDownloadMenus()
  })

  if (location.protocol === 'http:' || location.protocol === 'https:') {
    document.querySelectorAll('a.card-download').forEach(function (link) {
      fetch(link.href, { method: 'HEAD', cache: 'no-cache' })
        .then(function (response) {
          if (!response.ok) {
            link.classList.add('is-disabled')
            link.textContent = 'No disponible'
            link.removeAttribute('download')
          }
        })
        .catch(function () {})
    })

    document.querySelectorAll('.card-download-menu').forEach(function (root) {
      var links = Array.prototype.slice.call(
        root.querySelectorAll('.card-download-menu-panel a[href]'),
      )
      var label = root.querySelector('.card-download-menu-label')
      if (links.length === 0) return

      Promise.all(
        links.map(function (a) {
          return fetch(a.href, { method: 'HEAD', cache: 'no-cache' }).then(function (response) {
            return { a: a, ok: response.ok }
          })
        }),
      )
        .then(function (results) {
          var anyOk = false
          results.forEach(function (r) {
            if (!r.ok) {
              r.a.classList.add('is-disabled')
              r.a.removeAttribute('href')
              r.a.removeAttribute('download')
            } else anyOk = true
          })
          if (!anyOk) {
            root.classList.add('is-disabled')
            if (label) label.textContent = 'No disponible'
          }
        })
        .catch(function () {})
    })
  }
})()
