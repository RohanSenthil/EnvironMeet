//const events = [
//    { name: "rooftop gardening at tiong bahru"},
//    { name: "beach cleanup at east coast park"},
//    { name: "environmental workshop"},
//    { name: "save the turtles"},
//    { name: "recycling workshop"},
//    { name: "tree planting at yishun"},
//
//
//]
//
//const searchInput = document.getElementbyId("searchnput");
//
//const namesFromDom = document.getElementsbyClassName("title");
//
//searchInput.addEventListener("keyup", (event) =>) {
//    const { value } = event.target;
//
//    const searchQuery = value.toLowerCase();
//
//    for (const nameElement of namesFromDom) {
//        let name = nameElement.textContent.toLowerCase();
//
//        if (name.includes(searchQuery)) {
//           nameElement.stype.display = "block";
//        } else{
//          nameElement.stype.display = "none";
//        }
//    }
//}