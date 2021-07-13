// to store the element with class name "typed-text" for easier access
const typedTextSpan = document.querySelector(".typed-text")
// to store the element with class name "cursor" for easier access
const cursorSpan = document.querySelector(".cursor")
// array of strings to be displayed while typing
const textArray = ["to", "too", "two !"];
// delay between typing each character
const typingDelay = 200;
// delay between erasing each character
const erasingDelay = 100;
// delay between different strings
const newTextDelay = 2000;

// variable to store the index of the strings
let textArrayIndex = 0;
// variable to store the index of characters withing a string
let charIndex = 0;

function type(){
    if(charIndex < textArray[textArrayIndex].length){
        //type current string
        /*
        1. .textContent is used to acces the current contents of the "typed-text" element.
        2. the next character is added to this and charIndex is incremented.
        3. setTimeout() is used to call the function "type" again after "typingDelay" ms. 
        4. notice that "type" is a reference here and not a direct funciton call (it doesn't have round braces)
        */
        if(!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing");
        typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, typingDelay);
    }
    else{
        // remove the typing class name as we are about to start erasing
        cursorSpan.classList.remove("typing");
        //erase current string
        setTimeout(erase, newTextDelay);
    }
}

function erase(){
    if(charIndex > 0){
        typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex-1);
        charIndex--;
        setTimeout(erase, erasingDelay);
    }
    else{
        // add the typing class name as we are about to star typing
        cursorSpan.classList.add("typing");
        // type next string
        textArrayIndex++;
        if(textArrayIndex == textArray.length){
            textArrayIndex = 0;
            setTimeout(type, newTextDelay+2000);
        }
        else setTimeout(type, newTextDelay);
    }
}

document.addEventListener("DOMContentLoaded", function(){
    if(textArray.length) setTimeout(type, newTextDelay - 500 );
})