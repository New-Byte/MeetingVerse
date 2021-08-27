const date = new Date();

const renderCalendar = () => {
  date.setDate(1);

  const monthDays = document.querySelector(".days");

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  const prevLastDay = new Date(
    date.getFullYear(),
    date.getMonth(),
    0
  ).getDate();

  const firstDayIndex = date.getDay();

  const lastDayIndex = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDay();

  const nextDays = 7 - lastDayIndex - 1;

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  document.querySelector(".date h1").innerHTML = months[date.getMonth()] + " " + date.getFullYear();

  document.querySelector(".date p").innerHTML = new Date().toDateString();

  let days = "";

  for (let x = firstDayIndex; x > 0; x--) {
    days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDay; i++) {
    if (
      i === new Date().getDate() &&
      date.getMonth() === new Date().getMonth()
    ) {
      days += `<div class="today">${i}</div>`;
    } else {
      days += `<div onclick="try_new(this)">${i}</div>`;
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="next-date">${j}</div>`;
    monthDays.innerHTML = days;
  }
};

document.querySelector(".prev").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
  date.setMonth(date.getMonth() + 1);
  renderCalendar();
});

function try_new(x){
  var day = x.textContent;
  var month = date.getMonth() + 1;
  var year = date.getFullYear();
  document.getElementById("myForm").style.display = "block";
  var check = new Date(year, month-1,day).toDateString();
  if (check.slice(0,3) == "Sun"){
    window.alert("Employee is not available for meeting");
  }
  document.getElementById("add-date").value = year+"/"+month+"/"+day;
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

function show_time_slots(){
    
  document.getElementById("time_data").style.display = "block";

}

function save_data(y){
  var time_str = y.textContent;
  document.getElementById("time_data").style.display = "none";
  document.getElementById("add-time").value = time_str;
  document.getElementById("label1").style.display = "block";
  document.getElementById("add-time").style.display = "block";
  document.getElementById("time_slots").style.display = "none";
}
renderCalendar();
