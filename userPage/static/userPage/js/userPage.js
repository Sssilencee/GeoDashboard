const HOME_PAGE = 'http://127.0.0.1:8000/'


class InitPage {

  async checkLogin() {
    if (USER_SUBSCRIPTIONS == "") {

      await this.renderLoginPage()
      await this.addLoginPageListeners()

    } else {

      await this.renderHomePage()
      await this.renderUserSubscriptions().then(() => {this.addHomePageListeners()})

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

  }

  async addLoginPageListeners() {
    document.getElementById('logIn').onclick = function() {
      location.href = '/login'
    }
  }

  async addHomePageListeners() {

    document.getElementById('logOut').onclick = function(){
      location.href = '/logout';
    }

    document.querySelectorAll(".toolsList").forEach(item => {
      item.onclick = function() {

        let toolDescription = $(item.parentNode).find('.toolDescription')

        // Tool block: hide or show
        if (toolDescription[0].style.display == "block") {

          toolDescription.hide("fold", {direction:"top"}, 100)

        } else if (toolDescription[0].style.display == "") {

          toolDescription.show("fold", {direction:"top"}, 100)

        } else if (toolDescription[0].style.display == "none") {

          toolDescription.show("fold", {direction:"top"}, 100)

        }
      }
    })

    document.querySelectorAll('.unbind').forEach(item => {
      item.onclick = function() {

        let csrftoken = $.cookie('csrftoken'),
            xhr = new XMLHttpRequest(),
            key = item.parentNode.querySelector('p').innerText.split(/\s{4}/)[1].split('\n')[0]

        xhr.open('GET', 'http://127.0.0.1:8000/unbind', false)
        xhr.setRequestHeader('key', key)
        xhr.setRequestHeader("X-CSRFToken", csrftoken)

        xhr.send()

        if (xhr.status == 200) {
          window.location.href = HOME_PAGE
        }

      }
    })
  }

  async renderGroup(groupSubscriptions) {

    let groupDiv = document.createElement('div')

    let name = document.createElement('p')
    let description = document.createElement('p')

    let toolsContainer = document.createElement('div')

    let renewalDate = await this.cutString(USER_SUBSCRIPTIONS[groupSubscriptions].renewalDate, 10)

    groupDiv.innerHTML = "<img class=\"groupImg\" src='https://cdn.discordapp.com/icons/" +
                         USER_SUBSCRIPTIONS[groupSubscriptions].id + "/" +
                         USER_SUBSCRIPTIONS[groupSubscriptions].icon + ".png'/>"
    groupDiv.classList.add('groupDivList')

    name.innerHTML = await this.cutString(groupSubscriptions, 15)
    name.classList.add('groupNameList')

    description.innerHTML = "Renewal price   <span class='descriptionValueList'>" +
                            USER_SUBSCRIPTIONS[groupSubscriptions].renewalPrice +
                            "</span><br>Renewal date   <span class='descriptionValueList'>" +
                            renewalDate + "</span>"
    description.classList.add('groupDescriptionList')

    toolsContainer.classList.add('toolsContainer')

    groupDiv.appendChild(toolsContainer)
    groupDiv.appendChild(name)
    groupDiv.appendChild(description)

    return groupDiv

  }

  async renderGroupSubscriptions(groupSubscriptions, groupTool) {

    let toolDescription = document.createElement('p')
    let toolDescriptionContainer = document.createElement('div')
    let toolsDiv = document.createElement('div')

    let unbind = document.createElement('button')

    toolDescription.innerHTML = 'Key&nbsp&nbsp&nbsp&nbsp' +
                                USER_SUBSCRIPTIONS[groupSubscriptions].licenseKeys[groupTool].licenseKey +
                                '<br>' + 'Devices&nbsp&nbsp&nbsp&nbsp' +
                                USER_SUBSCRIPTIONS[groupSubscriptions].licenseKeys[groupTool].devices
    toolDescription.classList.add('toolDescription')

    toolsDiv.innerHTML = groupTool
    toolsDiv.classList.add('toolsList')

    unbind.innerHTML = 'Unbind'
    unbind.classList.add('unbind')
    unbind.classList.add('toolDescription')

    toolDescriptionContainer.classList.add('toolDescriptionContainer')
    toolDescriptionContainer.appendChild(toolsDiv)
    toolDescriptionContainer.appendChild(toolDescription)
    toolDescriptionContainer.appendChild(unbind)

    return toolDescriptionContainer
  }

  async renderUserSubscriptions() {

    let groupContainer = document.createElement('div')
    let mainData = document.createElement('div')

    for (let groupSubscriptions in USER_SUBSCRIPTIONS) {

      let groupDiv = await this.renderGroup(groupSubscriptions)
      let toolsContainer = groupDiv.querySelector('div')

      groupContainer.appendChild(groupDiv)

      for (let groupTool in USER_SUBSCRIPTIONS[groupSubscriptions].licenseKeys) {

        let toolDescriptionContainer = await this.renderGroupSubscriptions(groupSubscriptions, groupTool)
        toolsContainer.appendChild(toolDescriptionContainer)

      }
    }

    groupContainer.classList.add('groupContainerList')

    mainData.id = 'mainData'
    mainData.appendChild(groupContainer)

    document.body.appendChild(mainData)

  }

  async cutString(word, limit) {
    if (word.length > limit) {
      if (Array.from(word)[limit - 1] = ' ') {
        word = word.slice(0, limit - 3) + '..'
      } else {
        word = word.slice(0, limit - 2) + '..'
      }

    }
    return word
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
