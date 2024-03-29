function openTab(evt, LeaderboardType) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(LeaderboardType).style.display = "block";
  evt.currentTarget.className += " active";
}

function openGlobal(evt, GlobalType) {
  // Declare all variables
  var i, globalcontent, globallinks;

  // Get all elements with class="globalcontent" and hide them
  globalcontent = document.getElementsByClassName("globalcontent");
  for (i = 0; i < globalcontent.length; i++) {
    globalcontent[i].style.display = "none";
  }

  // Get all elements with class="globallinks" and remove the class "active"
  globallinks = document.getElementsByClassName("globallinks");
  for (i = 0; i < globallinks.length; i++) {
    globallinks[i].classList.remove("active");
  }

  // Show the current global, and add an "active" class to the button that opened the global
  document.getElementById(GlobalType).style.display = "block";
  evt.currentTarget.classList.add("active");
}

function openInvite(evt, InviteType) {
  // Declare all variables
  var i, invitecontent, invitelinks;

  // Get all elements with class="invitecontent" and hide them
  invitecontent = document.getElementsByClassName("invitecontent");
  for (i = 0; i < invitecontent.length; i++) {
    invitecontent[i].style.display = "none";
  }

  // Get all elements with class="invitelinks" and remove the class "active"
  invitelinks = document.getElementsByClassName("invitelinks");
  for (i = 0; i < invitelinks.length; i++) {
    invitelinks[i].classList.remove("active");
  }

  // Show the current invite, and add an "active" class to the button that opened the invite
  document.getElementById(InviteType).style.display = "block";
  evt.currentTarget.classList.add("active");
}

document.getElementById("defaultGlobalOpen").click();
document.getElementById("defaultAllTimeOpen").click();



