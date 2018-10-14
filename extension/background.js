const PURL = 'https://piazza.com/class'
let current = ''

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url && changeInfo.url.startsWith(PURL)) {
    let classId = changeInfo.url.slice(PURL.length + 1)

    if (classId) {
      let query = classId.indexOf('?')
      let cleanId = query == -1 ? classId : classId.slice(0, query)

      if (cleanId !== current) {
        current = cleanId

        httpRequest = new XMLHttpRequest()
        httpRequest.open('GET', `http://localhost:3000/preload/${cleanId}`, true)
        httpRequest.send()
      }
    }
  }
})