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
      let pop = res.data
      console.log(pop['score'])
      return (response.data);
    }).catch((err) => {
      console.log("Something went wrong ", err)
    })
    if (playerScore >= 38000) {
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
let lyrics = document.getElementById('line4').innerText // string of text
let blank = lyrics.replace(/[A-z]/gi, '_'); // blank string '___ _ __'
const punctuation = /[!"#$%&()*+,./:;<=>?@[\]^_`{|}~]/g;
let words = lyrics.replace(punctuation, '').split(' '); // aray of words ['word', 'word', 'word'], split punctuation
let sauce = blank.split(' '); // blank array ['___', '__', '___']
let genresBtn = document.getElementById('genres');

document.getElementById('guess').focus();
document.getElementById('guess').select();

genresBtn.style.visibility = 'hidden';

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
      sauce[idx] = lyrics.split(' ')[idx];
    });

    blank = sauce.join(' ');
    document.getElementById('ghost').innerText = blank;
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
let count = 60;

if (score !== null) {
  localStorage.setItem('score', '50000');
}

function timer() {

  count --;
  score -= 50;

  if (!blank.includes("_")) {
    clearInterval(counter);
    localStorage.setItem('score', $('#score').html());
    setTimeout(function () {
      genresBtn.style.visibility = 'visible';
      $('#guess')[0].disabled = true;
      alert("YOU REMEMBERED THE LYRICS! GOOD JOB!");
    }, 100);
  };

  if (count <= 0) {
    clearInterval(counter);
    localStorage.setItem('score', $('#score').html());
    setTimeout(function() {
      genresBtn.style.visibility = 'visible';

      $('#guess')[0].disabled = true;
      alert("I guess you forgot the lyrics this time.");
    }, 100);
  };

  document.getElementById('timer').innerHTML = count;
  document.getElementById('score').innerHTML = score;
}