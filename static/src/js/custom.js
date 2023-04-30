// Next
function nextSection() {
  var currentSection = document.querySelector(
    'section[style*="display: block"]'
  );

  if (currentSection.getAttribute("id") === "section1") {
    // document.getElementById('section2').scrollIntoView({behavior: 'smooth'});
    document.getElementById("section2").style.display = "block";
    document.querySelector(".color2").style.backgroundColor = "rgba(178, 219, 233, 0.432)";
  } else if (currentSection.getAttribute("id") === "section2") {
    document.getElementById("section3").style.display = "block";
    document.querySelector(".color3").style.backgroundColor = "rgba(178, 219, 233, 0.432)";
  }else if (currentSection.getAttribute("id") === "section3") {
    document.getElementById("section4").style.display = "block";
    document.querySelector(".color4").style.backgroundColor = "rgba(178, 219, 233, 0.432)";
  }else if (currentSection.getAttribute("id") === "section4") {
    document.getElementById("section4").style.display = "none";
    document.getElementById("section5").style.display = "block";
    document.querySelector("button:last-child").style.display = "none";
    document.querySelector(".color5").style.backgroundColor = "rgba(178, 219, 233, 0.432)"; // hide "next" button on last section
    
    }

  currentSection.style.display = "none";
  document.querySelector("button:first-child").style.display = "block"; // show "previous" button when moving forward
  document.body.scrollTop = document.documentElement.scrollTop = 0;
}
// Previous
function prevSection() {
  var currentSection = document.querySelector(
    'section[style*="display: block"]'
  );

  if (currentSection.getAttribute("id") === "section2") {
    document.querySelector(".color2").style.backgroundColor =
      "#d5caec57";
    document.getElementById("section1").style.display = "block";
    document.querySelector("button:first-child").style.display = "none"; // hide "previous" button on first section
  } else if (currentSection.getAttribute("id") === "section3") {
    document.querySelector(".color3").style.backgroundColor =
      "#d5caec57";
    document.getElementById("section2").style.display = "block";
    
  } else if (currentSection.getAttribute("id") === "section4") {
    document.querySelector(".color4").style.backgroundColor =
      "#d5caec57";
    document.getElementById("section3").style.display = "block";
    
  }else if (currentSection.getAttribute("id") === "section5") {
    document.querySelector(".color5").style.backgroundColor =
      "#d5caec57";
    document.getElementById("section4").style.display = "block";
    document.getElementById("section5").style.display = "none";
    document.querySelector("button:last-child").style.display = "block"; // show "next" button when moving back from last section
  }

  currentSection.style.display = "none";
  document.querySelector("button:last-child").style.display = "block"; // show "next" button when moving backward
  document.body.scrollTop = document.documentElement.scrollTop = 0;

}

// Addresses

const sameAsPermanentCheckbox = document.getElementById('same-as-permanent');
      const permanentAddressLine1 = document.getElementById('permanent-address');
      const permanentZipCode = document.getElementById('permanent-zip');
      const presentAddressLine1 = document.getElementById('present-address');
      const presentZipCode = document.getElementById('present-zip');
      
      sameAsPermanentCheckbox.addEventListener('change', function() {
        if (this.checked) {
          presentAddressLine1.value = permanentAddressLine1.value;
          presentZipCode.value = permanentZipCode.value;
        } 
        else {
          presentAddressLine1.value = '';
          presentZipCode.value = '';
        }
      });
  // Chart Js
// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart = new myChart(ctx, {
//     type: 'bar',
//     data: {
//         labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//         datasets: [{
//             label: '# of Votes',
//             data: [12, 19, 3, 5, 2, 3],
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.2)',
//                 'rgba(54, 162, 235, 0.2)',
//                 'rgba(255, 206, 86, 0.2)',
//                 'rgba(75, 192, 192, 0.2)',
//                 'rgba(153, 102, 255, 0.2)',
//                 'rgba(255, 159, 64, 0.2)'
//             ],
//             borderColor: [
//                 'rgba(255, 99, 132, 1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)'
//             ],
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero: true
//                 }
//             }]
//         }
//     }
// });