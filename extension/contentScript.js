console.log('hohohohohohohhoohoo')
let root = document.createElement('div')
root.classList.add('biazza')
document.querySelector('#views').appendChild(root)

let bar = document.createElement('div')
bar.classList.add('dashboard_toolbar', 'biazza_bbar')
bar.textContent = 'Biazza'
root.appendChild(bar)

let ul = document.createElement('ul')
root.appendChild(ul)


let page_center = document.querySelector('#page_center')
let keywordQueue = []
// root.classList.add('active')
// page_center.classList.add('active')
document.querySelector('#search-box').addEventListener('input', e => {
  if (e.target.value) {
    keywordQueue.push(e.target.value)
    root.classList.add('active')
    page_center.classList.add('active')
  }
  else {
    root.classList.remove('active')
    page_center.classList.remove('active')
  }
})
document.querySelector('#clear-search-button').addEventListener('click', () => {
  root.classList.remove('active')
  page_center.classList.remove('active')
})

function search() {
  if (!keywordQueue.length) return
  keyword = keywordQueue.pop()
  keywordQueue = []

  httpRequest = new XMLHttpRequest()
  httpRequest.onreadystatechange = () => {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
        while (ul.hasChildNodes()) {
          ul.removeChild(ul.firstChild)
        }
        for (node of JSON.parse(httpRequest.responseText)) {
          let li = document.createElement('li')
          li.classList.add('biazza_li')
          let title = document.createElement('div')
          title.classList.add('title', 'ellipses')
          title.textContent = node.sub
          li.appendChild(title)
          let short = document.createElement('div')
          short.classList.add('short')
          short.textContent = node.short
          li.appendChild(short)
          ul.appendChild(li)
        }
      }
    }
  }
  httpRequest.open('GET', `http://localhost:3000/search?key=${keyword}&cid=${window.location.pathname.slice(7)}`, true)
  httpRequest.send()
  console.log(keyword)
}
setInterval(search, 1000)