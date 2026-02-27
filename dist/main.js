// Update title
(() => {
  let state = false
  const header = document.getElementById('header')
  const update = () => {
    state = !state
    let content = state ? ">\u00A0" : "\u00A0\u00A0"
    content += "IEEE Searchbot Console"
    header.textContent = content
    setTimeout(update, 1000)
  }
  setTimeout(update, 1000)
})()
