// Click on the "Jeans" link on page load to open the accordion for demo purposes
document.getElementById("myBtn").click();

function showId(ID) {
    //console.log("showId::", ID)
    document.getElementById(ID).style.display = "block";
}

function hideId(ID) {
    //console.log("hideId::", ID)
    document.getElementById(ID).style.display = "none";
}

var slideIndex = 0;
showSlides();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    console.log("slides:", slides)
    console.log("dots:", dots)
        //if (slides.length != 0) {

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += "active";
    setTimeout(showSlides, 3000); // Change image every 2 seconds
    //}
}
