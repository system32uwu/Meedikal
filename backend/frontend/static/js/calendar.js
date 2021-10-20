let _callback = () => {};

options = {};
options.endpoint = "/api/appointment/all";
options.body = {};
options.method = "POST";

let selectedMonth = CURRENT_MONTH;
let selectedYear = CURRENT_YEAR;
let selectedDay = CURRENT_DAY;
let previousSelectedDay;

let _calendar;

const firstWeekDayOfMonth = () =>
  new Date(selectedYear, selectedMonth).getDay();

const generateCalendar = () => {
  let calendar = document.getElementById(_calendar);
  let daysBtns = Date.prototype.getDaysList(selectedMonth).map((v) => {
    let container = document.createElement("div");
    container.innerHTML = generateDayChip(v);
    return container;
  });
  console.log(selectedMonth, daysBtns)
  daysBtns[0].classList.add(`col-start-${firstWeekDayOfMonth()}`);

  calendar.innerHTML = `  
                        <span class="px-2 w-8 font-semibold">Mon</span>
                        <span class="px-2 w-8 font-semibold">Tue</span>
                        <span class="px-2 w-8 font-semibold">Wed</span>
                        <span class="px-2 w-8 font-semibold">Thu</span>
                        <span class="px-2 w-8 font-semibold">Fri</span>
                        <span class="px-2 w-8 font-semibold">Sat</span>
                        <span class="px-2 w-8 font-semibold">Sun</span>`;

  daysBtns.map((d) => calendar.appendChild(d));
};

const fetchAppointments = async (day) => {
  selectedDay = day;
  if (previousSelectedDay) {
    previousSelectedDay.classList.remove("bg-turqoise");
    previousSelectedDay.classList.add("text-gray-500");
  }

  let dayBtn = document.getElementById(day);

  dayBtn.classList.add("bg-turqoise");
  dayBtn.classList.remove("text-gray-500");
  dayBtn.classList.add("text-white");

  previousSelectedDay = dayBtn;

  _callback('DAY', new Date(selectedYear, selectedMonth, selectedDay));
};

const generateDropDowns = (monthYearSelectors, monthSelect, yearSelect) => {
  let mySelectors = document.getElementById(monthYearSelectors);
  mySelectors.innerHTML = generateDropDown(monthSelect, MONTHS);
  mySelectors.innerHTML += generateDropDown(yearSelect, YEARS);
  
  document.getElementById(monthSelect).onchange = (ev) => {
    selectedMonth = parseInt(ev.target.value);
    refreshCalendar();
    _callback('MONTH', new Date(selectedYear, selectedMonth, selectedDay));
  };

  document.getElementById(yearSelect).onchange = () => {
    selectedYear = this.value;
    _callback('YEAR', new Date(selectedYear, selectedMonth, selectedDay));
  };
};

const refreshCalendar = (calendar) => {
  generateCalendar(calendar);
  fetchAppointments(selectedDay);
}

const initCalendar = (
  monthYearSelectors,
  monthSelect,
  yearSelect,
  calendar,
  callback
) => {
  _callback = callback;
  _calendar = calendar;
  generateDropDowns(monthYearSelectors, monthSelect, yearSelect);
  refreshCalendar();
};
