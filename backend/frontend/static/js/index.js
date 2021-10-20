const PHONE_REGEX = /^[\+]?[0-9]*/;

const RUNNING_SINCE = 2021;

const TODAY = new Date();

const CURRENT_MONTH = TODAY.getMonth();

const CURRENT_YEAR = TODAY.getFullYear();

const CURRENT_DAY = TODAY.getDate();

const CURRENT_WEEKDAY = TODAY.getDay();

Date.locale = {
  en: {
    monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    dayNames: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  },
  es: {
    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    dayNames: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
  }
};

Date.prototype.getMonthName = (number, lang='en') => {
  return Date.locale[lang].monthNames[number];
};

Date.prototype.getMonthNumber = (name, lang='en') => {
  return Date.locale[lang].monthNames.indexOf(name);
};

Date.prototype.getMonthDays = (monthNumber) => {
  let d = new Date(CURRENT_YEAR, monthNumber + 1, 0);
  return d.getDate();
}

Date.prototype.getDaysList = (monthNumber) => {
  let dayCount = Date.prototype.getMonthDays(monthNumber);
  return Array.from({length: dayCount}, (_, i) => i+1);
}

Date.prototype.getDayName = (date, lang='en') => {
  return date.toLocaleString(lang, {weekday:'short'})
}

const YEARS = Array.from(Array(CURRENT_YEAR + 5 - RUNNING_SINCE), (_, i) => ({
    value: i + RUNNING_SINCE,
    label: i + RUNNING_SINCE,
    selected: i + RUNNING_SINCE === CURRENT_YEAR,
  }));
  
const MONTHS = Array.from(Array(12).keys()).map((v) => ({
    value: v,
    label: Date.prototype.getMonthName(v),
    selected: v === CURRENT_MONTH ? true : false,
}));

const nameCell = (name, photoUrl) => `
    <td class="px-6 py-4 whitespace-nowrap">
      <div class="flex items-center">
        <div class="flex-shrink-0 h-10 w-10">
          <img
            class="h-10 w-10 rounded-full"
            src="${photoUrl || "/static/images/user-placeholder.png"}"
          />
        </div>
        <div class="ml-4">
          <div class="text-sm font-medium text-gray-900">
            ${name}
          </div>
        </div>
      </div>
    </td>
    `;

const generateActiveCell = (userId, value, fn) => `
      <td class="px-6 py-4 whitespace-nowrap">
        <div class="text-sm text-gray-900 text-center">
          ${
            fn
              ? `
            <button onclick="${fn}(${userId})" class="focus:outline-none">
              <span id="active-${userId}" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  value ? "bg-green-100" : "bg-red-100"
                } text-green-800">
                ${value ? "Active" : "Inactive"}
              </span> 
            </button>`
              : `
            <span id="active-${userId}" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  value ? "bg-green-100" : "bg-red-100"
                } text-green-800">
              ${value ? "Active" : "Inactive"}
            </span> 
            `
          }
        </div>
      </td>`;

const generateActionsCell = (id, fnSuffix) => `
    <td>
      <div class="flex space-x-2 justify-center">
        <button class="rounded-full hover:bg-gray-300 px-2 py-2" onclick="delete${fnSuffix}(${id})">
          <img src="/static/icons/delete.svg" width="16"/>
        </button>
        <button class="rounded-full hover:bg-gray-300 px-2 py-2" onclick="update${fnSuffix}(${id})">
          <img src="/static/icons/edit.svg" width="16"/>
        </button>
      </div>
    </td
`;

const generateColumn = (colName) => `
      <th scope="col" id="${colName}" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
        ${colName}
      </th>`;

const generateCell = (value) => `
      <td class="px-6 py-4 whitespace-nowrap">
        <div class="text-sm text-gray-900 text-center">
            ${value}
        </div>
      </td>`; //generic cell generator

const generateRow = (cells, rowId) => `
    <tr id="row-${rowId}">
        ${cells.join("\n")}
    </tr>
    `;

const generateTable = (tableId, colNames, rows) => `
    <div class="border-b border-gray-200 sm:rounded-lg overflow-y-auto h-full">
        <table class="divide-y divide-gray-200 w-full h-full" id="${tableId}">
            <thead class="bg-gray-50">
                <tr>
                    ${colNames.map((name) => generateColumn(name)).join("\n")}
                </tr>
            </thead>
            <tbody>
                ${rows.join("\n")}
            </tbody>
        </table>
    </div>
    `;

    const generatePhoneChip = (value) => `
    <div id='${value}' class="inline-flex items-center rounded-full border border-gray-200 px-1 py-2 bg-turqoise h-8">
        <span class="px-1 w-full leading-none text-white text-center text-white font-bold">
            ${value}
        </span>
        <button onclick="deletePhone(${value})" class="h-5 w-5 rounded-full bg-opacity-25 focus:outline-none">
            <img src="/static/icons/delete.svg" width="16" height="16" />
        </button>
    </div>
    `;

const generateSpecialtiesField = (chips) => `
<div class="flex h-full">
  <span class="text-sm border bg-blue-50 font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">
    Specialties
  </span>
  <div class="shadow-sm flex flex-wrap items-center justify-center md:justify-start px-4 gap-1 w-4/6">
    <div class="flex flex-row w-full" id="container-Specialties">
      ${chips}
    </div>
    <div class="inline-flex items-center rounded-full border border-gray-200 px-1 py-2 h-8">
      <div>
        <input id='new-Specialties' type="text" class="px-1 w-full text-black text-center focus:outline-none" value=""/> 
      </div>
      <button onclick="addSpecialty()" class="h-5 w-5 rounded-full bg-opacity-25 focus:outline-none">
        <img src="/static/icons/add.svg" width="16" height="16" class="-mx-1"/>
      </button>
    </div>  
  </div>
</div>
    `;

const generateSpecialtyChip = (value) => `
    <div id='${value}' class="inline-flex items-center rounded-full border border-gray-200 px-1 py-2 bg-turqoise h-8">
      <span class="px-1 w-full leading-none text-white text-center text-white font-bold">
          ${value}
      </span>
      <button onclick="deleteSpecialty('${value}')" class="h-5 w-5 rounded-full bg-opacity-25 focus:outline-none">
          <img src="/static/icons/delete.svg" width="16" height="16" />
      </button>
    </div>
    `;

const generateRoleChip = (value, roleColor) => `
    <div id="${value}" class="inline-flex items-center rounded-full border border-gray-200 px-1 py-2 ${roleColor} h-8">
      <span class="px-1 w-full leading-none text-white text-center font-bold">
        ${value}
      </span>
      <button onclick="toggleRole('${value}')" class="h-5 w-5 rounded-full bg-opacity-25 focus:outline-none">
            <img id="icon-${value}" src="/static/icons/add.svg" width="16" height="16" />
      </button>
    </div>
        `;

const generateDayChip = (value) => `
    <div class="inline-flex items-center rounded-full px-1 py-2 h-8">
      <button id="${value}" onclick="fetchAppointments(${value})" class="h-6 w-8 rounded-full focus:outline-none hover:bg-turqoise hover:text-white text-gray-500">
        <span class="px-1 w-full leading-none text-center">
          ${value}
        </span>
      </button>
    </div>
`;

const generateDropDown = (id, options) => `
    <div class="relative inline-flex">
        <svg class="w-2 h-2 absolute top-0 right-0 m-4 pointer-events-none" xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 412 232">
            <path d="M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9.763 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.323 17.677 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 9.763-25.592 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 171.144z" fill="#648299" fill-rule="nonzero" />
        </svg>
        <select id='${id}' class="border border-gray-300 rounded-lg text-gray-600 h-10 pl-5 pr-10 bg-white hover:border-gray-400 focus:outline-none appearance-none">
          ${options.map((op) =>
            op.selected
              ? `<option value=${op.value ? op.value : op} selected>${op.label ? op.label : op}</option>`
              : `<option value=${op.value ? op.value : op}>${op.label ? op.label : op}</option>`
          )}
        </select>
    </div>
`;

const setPagination = async (
  tablename,
  offset,
  limit,
  paginationContainer,
  fn,
  conditions=null
) => {
  let options = {};

  options.headers =  {
    Accept: "application/json",
    "Content-Type": "application/json",
  }

  if (conditions){
    try{
      options.body = JSON.stringify(conditions)
      options.method = 'POST';
    }catch(e){
      options.body = {};
    }
  }

  res = await fetch(`/api/pagination/total/${tablename}`, options);

  data = await res.json();

  if (res.status === 200) {

    let total = data.result;
    if (total < 1){
      paginationContainer.innerHTML = '';
      return 0;
    }

    if (total < limit) {
      limit = total;
    }

    let itemsPerPage = limit - offset;

    let pageCount = total / itemsPerPage;

    let btns = Array(Math.ceil(pageCount)); //round up

    for (let i = 0; i < pageCount; i++) {
      btns.push(`
              <button 
              class="rounded-xl bg-turqoise text-white font-bold px-2 text-center"
              onclick='${fn}(${itemsPerPage * i} ${options.body ? ', ' + options.body : null})'>
              ${i + 1}
              </button>
            `);
    }
    paginationContainer.innerHTML = btns.join("\n");
    return total;
  } else {
    Promise.reject(res.data);
  }
};

const toggleLoadingModal = (forceHide = false, forceShow = false) => {
  const loadingModal = document.getElementById("loading-modal");
  if (forceHide) {
    loadingModal.classList.add("hidden");
  } else if (forceShow) {
    loadingModal.classList.remove("hidden");
  } else {
    loadingModal.classList.toggle("hidden");
  }
};

const delay = (time) => {
  return new Promise((resolve) => setTimeout(resolve, time));
};

const showOkModal = async (
  title = "Operation Successful",
  body = "You may keep operating now"
) => {
  toggleLoadingModal(true);
  const okModal = document.getElementById("ok-modal");

  document.getElementById("ok-modal-title").textContent = title;
  document.getElementById("ok-modal-body").textContent = body;
  okModal.classList.remove("hidden");

  delay(500).then(() => {
    window.location.href = window.location.href; //force reload on page
  });
};
