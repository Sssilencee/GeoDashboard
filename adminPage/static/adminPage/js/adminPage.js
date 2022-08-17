const ADMIN_PAGE = 'http://127.0.0.1:8000/nothingInteresting'

const DELETE_KEY = 'http://127.0.0.1:8000/nothingInteresting/delete'
const DELETE_INVITE = 'http://127.0.0.1:8000/nothingInteresting/deleteInvite'


class InitPage {

  async checkLogin() {
    if (USER_DATA == "") {

      await this.renderLoginPage()
      await this.addLoginPageListeners()

    } else {

      await this.renderHomePage()
      await this.addGroupsToSelect()
      await this.addCreateListeners()
      await this.addMenuListeners().then(() => {this.addHomePageListeners()})

    }
  }

  async renderLoginPage() {
    document.getElementById('auth').style.display = 'block'
    document.getElementById('home').style.display = 'none'
  }

  async renderHomePage() {

    document.getElementById('auth').style.display = 'none'
    document.getElementById('home').style.display = 'block'

    document.querySelector('body').style.backgroundColor = "#1A1A1A"
    document.querySelector('body').style.backgroundImage = 'none'

    document.getElementById('discordLogin').innerHTML = USER_DATA.username
    document.getElementById('profileImage').src = 'https://cdn.discordapp.com/avatars/' + USER_DATA.id +
                                                  '/' + USER_DATA.avatar +'.png'

    let licenseKeyElementList = document.getElementsByClassName('licenseKeyDivElement')

    for (let i = 0; i < 4; i++) {

      let rect = licenseKeyElementList[i].getBoundingClientRect();
      document.getElementsByClassName('mainDataDescription')[i].style.left = rect.left + 10 + 'px'

      document.getElementById('adminKey').value = ADMIN_KEY
      document.getElementById('adminKeyInvite').value = ADMIN_KEY

    }

  }

  async addLoginPageListeners() {
    document.getElementById('logIn').onclick = function() {
      location.href = '/nothingInteresting/login'
    }
  }

  async addHomePageListeners() {

    document.getElementById('logOut').onclick = function(){
      location.href = '/nothingInteresting/logout';
    }

    document.querySelectorAll('.delete').forEach(item => {
      item.onclick = function() {

        let csrftoken = $.cookie('csrftoken'),
            xhr = new XMLHttpRequest(),
            key = item.getAttribute('data')

        xhr.open('POST', DELETE_KEY, false)
        xhr.setRequestHeader('deleteKey', key)
        xhr.setRequestHeader("X-CSRFToken", csrftoken)

        xhr.send()

        if (xhr.status == 200) {
          window.location.href = ADMIN_PAGE
        }

      }
    })

    document.querySelectorAll('.deleteinvites').forEach(item => {
      item.onclick = function() {

        let csrftoken = $.cookie('csrftoken'),
            xhr = new XMLHttpRequest(),
            key = item.getAttribute('data')

        xhr.open('POST', DELETE_INVITE, false)
        xhr.setRequestHeader('deleteKey', key)
        xhr.setRequestHeader("X-CSRFToken", csrftoken)

        xhr.send()

        if (xhr.status == 200) {
          window.location.href = ADMIN_PAGE
        }

      }
    })

    document.getElementById('blur').onclick = async function() {

      document.getElementById('createInvite').style.display = 'none'
      document.getElementById('bindKeyWindow').style.display = 'none'
      document.getElementById('blur').style.display = 'none'

    }

  }

  async addGroupsToSelect() {

    for (let i = 0; i < GROUPS.length; i++) {

      let option = document.createElement('option')

      option.value = GROUPS[i]
      option.innerHTML = GROUPS[i]

      document.getElementById('group').appendChild(option)

    }

    for (let i = 0; i < GROUPS.length; i++) {

      let option = document.createElement('option')

      option.value = GROUPS[i]
      option.innerHTML = GROUPS[i]

      document.getElementById('groupInvite').appendChild(option)

    }

  }

  async addCreateListeners() {

    document.getElementById('bindNewKey').onclick = async function() {

      document.getElementById('bindKeyWindow').style.display = 'block'
      document.getElementById('blur').style.display = 'block'

      function makeid(length) {

        let result           = ''
        let characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        let charactersLength = characters.length

        for (let i = 0; i < length; i++) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength))
        }

        return result

      }

      // Random key generator
      document.getElementById('key').value = makeid(4) + '-' + makeid(4) + '-' + makeid(4) + '-' +makeid(4)
      document.getElementById('devices').value = '0/1'

    }

    document.getElementById('createInviteButton').onclick = async function() {

      document.getElementById('createInvite').style.display = 'block'
      document.getElementById('blur').style.display = 'block'

      document.getElementById('devices').value = '0/1'

    }

  }

  async addMenuListeners() {

    let keysLine = document.getElementById('keysLine')
    let invitesLine = document.getElementById('invitesLine')

    let mainHeader = document.getElementById('mainHeader')
    let mainHeaderInvites = document.getElementById('mainHeaderInvites')

    let mainData = document.getElementById('mainData')
    let invites = document.getElementById('invites')

    let menuKeys = document.getElementById('menuKeys')
    let menuInvites = document.getElementById('menuInvites')

    document.getElementById('menuKeys').onclick = async function() {

      keysLine.style.display = 'block'
      invitesLine.style.display = 'none'

      mainHeader.style.display = 'block'
      mainHeaderInvites.style.display = 'none'

      mainData.style.display = 'block'
      invites.style.display = 'none'

      menuKeys.style.color = '#FFFFFF'
      menuInvites.style.color = '#B3B3B3'

    }

    document.getElementById('menuInvites').onclick = async function() {

      keysLine.style.display = 'none'
      invitesLine.style.display = 'block'

      mainHeader.style.display = 'none'
      mainHeaderInvites.style.display = 'block'

      mainData.style.display = 'none'
      invites.style.display = 'block'

      menuKeys.style.color = '#B3B3B3'
      menuInvites.style.color = '#FFFFFF'

      let invitesElementList = document.getElementsByClassName('invitesDivElement')

      for (let i = 0; i <= 3; i++) {

          let rect = invitesElementList[i].getBoundingClientRect()
          document.getElementsByClassName('invitesDescription')[i].style.left = rect.left + 10 + 'px'

      }

    }

  }

}


window.onload = function() {

  Page = new InitPage()
  Page.checkLogin()

  setTimeout(() => {
    let blur = document.getElementById('loading')

    blur.style.opacity = 0
    blur.style.visibility = 'hidden'
    blur.style.webkitTransition = 'visibility 0.5s linear, opacity 0.5s linear'
  }, 1000)

}
