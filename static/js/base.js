function handleChange(elem) {
    const sendButton = elem.parentNode.nextSibling.nextSibling.getElementsByTagName('button')[1]
    elem.value.length ? sendButton.disabled = false : sendButton.disabled = true
}

function setComment(elem) {
    const commentaryTextarea = elem.parentNode.previousSibling.previousSibling.getElementsByTagName('textarea')[0]
    const commentary = elem.value
    const body = commentaryTextarea.value
    if (elem.innerText === 'Коментировать') {
        elem.disabled = true
        commentaryTextarea.style.display = 'block'
        elem.innerText = 'Отправить'
    } else {
        if (body && commentary) {
            sendSubComment(commentary, body)
        }
        commentaryTextarea.style.display = 'none';
        commentaryTextarea.value = ''
        elem.innerText = 'Коментировать'
    }
}

function fetchSubComments(elem) {
    const commentary = elem.value
    const subDiv = elem.parentNode.nextSibling.nextSibling

    if (elem.innerText === 'Больше') {
        fetchAllSubComments(commentary, subDiv)

        elem.innerText = 'Скрыть'
    } else {
        elem.innerText = 'Больше'
        subDiv.innerHTML = ''
    }
}

function fetchAllSubComments(commentary, div) {
    fetch(`/commentary/${commentary}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(res => res.json())
        .then(data => {
            data['sub_comment'] && data['sub_comment'].map(el => (
                div.innerHTML += `
                        <div class='sub'><p>${new Date(el.timestamp).toLocaleString()}</p><p>${el.body}<p></div>
                        `
            ))
        })
        .catch(error => console.log(error))
}

function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='))

  if (xsrfCookies.length === 0) {
    return null
  }
  return decodeURIComponent(xsrfCookies[0].split('=')[1])
}

const csrfToken = getCookie('csrftoken')

function sendSubComment(commentary, body) {
    fetch('/add-sub/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({commentary, body})
    })
        .then(res => console.log(res.json()))
        .catch(error => console.log(error))
}
