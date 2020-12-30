const BASE_URL = "http://localhost:5000"

const genres = document.querySelectorAll('.box.genre');

let score = localStorage.getItem('score') || 50000;

genres.forEach(genre => {
  const boxClass = sessionStorage.getItem(genre.id);
  if (boxClass !== null) {
    genre.className = boxClass;
  }
  genre.onclick = function() {
    sessionStorage.setItem(genre.id, 'box genre completed');
  }
  if ($('.box.genre').length === $('.box.genre.completed').length) {
    playerScore = localStorage.getItem('score')
    axios({
      method: 'post',
      url: '/jsonres',
      headers: { "Content-Type" : "application/json" },
      data: {
        "score" : parseInt(playerScore)
      }
    }).then(function (response) {
      //data = JSON.parse(data.config.data); // this is the part i need config.data
      data = JSON.parse(response.config.data);
      res = response
      console.log(data['score']);
      console.log(res)
      console.log("********************")
      let pop = res.data
      console.log(pop['score'])
      return (response.data);
    }).catch((err) => {
      console.log("NO SOUP FOR YOU!!", err)
    })
    if (playerScore > 48000) {
      window.location = '/genres/Bonus'
    } else {
      window.location = '/game-over'
    }
  }
});

function clearStorage() {
  sessionStorage.clear();
  localStorage.clear();
}

$('#game-over').on('click', function() {
  console.log("end button clicked!!")
  sessionStorage.clear();
  localStorage.clear();
  window.location.href = "/genres";
})

$(document).ready(function() {
  $('#login').click(clearStorage);
  $('#signup').click(clearStorage)
})



// **********************This works just uncomment these lines!!**********************
let lyrics = document.getElementById('line3').innerText // string of text
let blank = lyrics.replace(/[A-z]/gi, '_'); // blank string '___ _ __'
let words = lyrics.split(/\s*\b\s*/); // aray of words ['word', 'word', 'word'], split punctuation
let sauce = blank.split(/\s*\b\s*/); // blank array ['___', '__', '___']
let genresBtn = document.getElementById('genres');
// regex v.2 = .replace(/[^\w\s]|_/g, "").replace(/\s+/g, " ")
// regex v.3 = .split(/\s*\b\s*/)
document.getElementById('guess').focus();
document.getElementById('guess').select();

genresBtn.style.visibility = 'hidden';
console.log(words);
document.addEventListener('keydown', event => {
  if (event.code === 'Space') {
    event.preventDefault();

    let userInput = $('#guess').val();
  
    const matchIdx = [];

    if (words.join(' ').toLowerCase().includes(userInput)) {
      document.getElementById('guess').style.borderBottom = '2px solid green';
    } else {
      document.getElementById('guess').style.borderBottom = '2px solid red';
    }

    words.forEach((word, idx) => {
        if (userInput === word.toLowerCase()) { // check punct list word
          matchIdx.push(idx);
        }
    });

    matchIdx.forEach(idx => {
      sauce[idx] = words[idx];
    });

    blank = sauce.join(' ');
    document.getElementById('ghost').innerText = blank;
    console.log(blank)
    document.getElementById('word-form').reset();
  };
});


document.addEventListener('keydown', event => {
  if (event.code === 'Enter') {
    event.preventDefault();
  }
});


// -------------Code for Timer/Score--------------------->>>>>>>>

let counter = setInterval(timer, 1000);
let count = 4;

if (score !== null) {
  localStorage.setItem('score', '50000');
}
// let points = document.getElementById('score').innerHTML;

function timer() {

  count --;
  score -= 50;

  if (!blank.includes("_")) {
    clearInterval(counter);
    localStorage.setItem('score', $('#score').html());
    setTimeout(function () {
      genresBtn.style.visibility = 'visible';
      alert("WINNER WINNER CHICKEN DINNER!");
    }, 100);
  };

  if (count <= 0) {
    clearInterval(counter);
    localStorage.setItem('score', $('#score').html());
    setTimeout(function() {
      genresBtn.style.visibility = 'visible';
      alert("Times UP BUCKO!");
    }, 100);
  };

  document.getElementById('timer').innerHTML = count;
  document.getElementById('score').innerHTML = score;
}