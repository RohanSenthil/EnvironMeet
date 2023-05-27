fuction openTab event(evt, LeaderboardType){
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++){
        tabcontent[i].style.display="none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0;i < tablinks.length; i++){
        tablinks[i].className = tanblinks[i].className.replace("active", "");
    }

    document.getElementsById(LeaderboardType).style.display = "block";
    evt.currentTarget.className += "active";

}