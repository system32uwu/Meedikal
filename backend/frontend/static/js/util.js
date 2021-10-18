const phoneRegex = /^[\+]?[0-9]*/;

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
