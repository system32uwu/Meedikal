const phoneRegex = /^[\+]?[0-9]*/;

const generateColumn = (colName) =>`
    <th scope="col" id="${colName}" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
      ${colName}
    </th>`;

const generateCell = (value) => `
    <td class="px-6 py-4 whitespace-nowrap">
      <div class="text-sm text-gray-900 text-center">
          ${value}
      </div>
    </td>`; //generic cell generator

const generateRow = (cells) => `
    <tr>
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

const setPagination = async (
  tablename,
  offset,
  limit,
  paginationContainer,
  fn
) => {
  res = await fetch(`/api/pagination/total/${tablename}`);
  data = await res.json();

  if (res.status === 200) {
    total = data.result;

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
              onclick="${fn}(${itemsPerPage * i})">
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
