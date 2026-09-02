const form = document.getElementById("signupForm");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const signupMessage = document.getElementById("signupMessage");



const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

form.addEventListener("submit" , function(event){
    event.preventDefault();


    const name = nameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;




if(name === "" || email === "" || password ===""){
    signupMessage.textContent="Please fill all fields";
} else if(!emailPattern.test(email)){
    signupMessage.textContent="Invalid email";
}else{
    signupMessage.textContent="All fields are valid";
}
});

const searchInput = document.getElementById("searchInput");
const books = document.querySelectorAll(".book");
const searchMessage = document.getElementById("searchMessage")
searchInput.addEventListener("input" , function(){
    const searchtext = searchInput.value.trim().toLowerCase();
    let foundbooks = 0;
    books.forEach(function (book) {
        const booktext = book.textContent.toLowerCase();
        if(booktext.includes(searchtext)){
            book.style.display="";
            foundbooks++;
        }else{
            book.style.display="none"
        }
    });
    if(searchtext ===""){
        searchMessage.textContent = "" ;
    }else if(foundbooks === 0){
         searchMessage.textContent = "No books found";
    }else if (foundbooks === 1) {
         searchMessage.textContent = "1 book found";
    }else{
        searchMessage.textContent = foundbooks + " BOOKS FOUND";
    }
});


