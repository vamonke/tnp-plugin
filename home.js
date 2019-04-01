const monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
const dayNames = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
let today = new Date();
let currentHour = today.getHours();
let currentMonth = today.getMonth()
let currentDate = today.getDate();
let currentDay = today.getDay();

// $(function() {
  console.log("home.js");
  
  let greeting;  
  if (currentHour < 12) {
    greeting = 'Morning';
    nextEdi = '12pm';
  } else if (currentHour < 18) {
    greeting = 'Afternoon';
    nextEdi = '6pm';
  } else {
    greeting = 'Evening'
    nextEdi = '9am';
  }

  $('#greeting').text(greeting);
  $('#date').text(currentDay + ' ' + monthNames[currentMonth]);
  $('#day').text(dayNames[currentDay]);
  $('#next-edi-timing').text(nextEdi);

  $('.mood-picker').hide();
  $('#' + greeting).show();

  var n_featured = 3;
  // GET featured
  function loadFeatured(stories) {
    console.log(stories);
    n_featured = stories.length;
    stories.forEach(story => {
      const html = `
        <div class="featured" style="background-image: url(${story.img_src})">
          <div class="overlay">
            <div class="category">${story.category}</div>
            <div class="news-title">${story.headline}</div>
            <div class="bottom">
              <a href="${story.url}" class="read">READ</a>
              <div class="date">
                ${story.published_date}
                <span class="divider">|</span>
                ${story.tag}
              </div>
            </div>
          </div>
        </div>
      `;
      $(".featured-container").append(html);
    });

    // Interactions

    let showing = 0;
    let featuredTiles = $(".featured-container").children();
    toggleTiles();

    function toggleTiles() {
      let target = featuredTiles[showing];
      $(target)
        .show()
        .siblings("div")
        .hide();

      $("#right-arrow, #left-arrow").removeClass("disabled");
      if (showing == 0) {
        $("#left-arrow").addClass("disabled");
      } else if (showing == n_featured) {
        $("#right-arrow").addClass("disabled");
      }
    }

    $("#right-arrow").click(function() {
      if (showing < n_featured) showing += 1;
      toggleTiles();
    });

    $("#left-arrow").click(function() {
      if (showing > 0) showing -= 1;
      toggleTiles();
    });
  }

  $.ajax({
    url: "http://127.0.0.1:5000/api/breaking",
    method: "GET",
    crossDomain: true,
    contentType: "application/json",
    dataType: "json",
    responseType: "application/json",
    success: loadFeatured,
    error: function(xhr, textStatus, errorThrown) {
      console.log(xhr);
      console.log(textStatus);
      console.log(errorThrown);
    }
  });

  $('.mood').click(function() {
    // console.log(this);
    var mood = $(this).attr('id');
    window.location.href= "stories.html?mood=" + mood;
  })
  
  $('#close-icon').click(function() {
    console.log('close');
    window.close();
  })

// });
