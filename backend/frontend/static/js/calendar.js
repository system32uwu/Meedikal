let _callback = () => {};

options = {};
options.endpoint = "/api/appointment/all";
options.body = {};
options.method = "POST";

let selectedMonth = CURRENT_MONTH;
let selectedYear = CURRENT_YEAR;
let selectedDay = CURRENT_DAY;
let previousSelectedDay;

const firstWeekDayOfMonth = () =>
  new Date(selectedYear, selectedMonth).getDay();

const generateCalendar = (calendarId) => {
  let calendar = document.getElementById(calendarId);
  let daysBtns = Date.prototype.getDaysList(selectedMonth).map((v) => {
    let container = document.createElement("div");
    container.innerHTML = generateDayChip(v);
    return container;
  });

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

  _callback(day);
};

const generateDropDowns = (monthYearSelectors, monthSelect, yearSelect) => {
  let mySelectors = document.getElementById(monthYearSelectors);
  mySelectors.innerHTML += generateDropDown(monthSelect, MONTHS);
  mySelectors.innerHTML += generateDropDown(yearSelect, YEARS);
};

const initCalendar = (
  monthYearSelectors,
  monthSelect,
  yearSelect,
  calendar,
  callback
) => {
  _callback = callback;
  generateDropDowns(monthYearSelectors, monthSelect, yearSelect);
  generateCalendar(calendar);
  fetchAppointments(selectedDay, _callback);
};
