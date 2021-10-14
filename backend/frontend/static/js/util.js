const generateColumn = (colName) => {
    return `
    <th
    scope="col"
    id="${colName}"
    class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
    ${colName}
    </th>`
};

const generateCell = (value) => {
    return `
    <td class="px-6 py-4 whitespace-nowrap">
    <div class="text-sm text-gray-900 text-center">
        ${value}
    </div>
    </td>`;
} //generic cell generator

const generateRow = (cells) => {
    return `
    <tr>
        ${cells.join("\n")}
    </tr>
    `;
}

const generateTable = (tableId, colNames, rows) => {
    return `
    <div class="border-b border-gray-200 sm:rounded-lg overflow-y-auto h-full">
        <table class="divide-y divide-gray-200 w-full h-full" id="${tableId}">
            <thead class="bg-gray-50">
                <tr>
                    ${colNames.map((name) => generateColumn(name)).join('\n')}
                </tr>
            </thead>
            <tbody>
                ${rows.join("\n")}
            </tbody>
        </table>
    </div>
    `;
}

const setPagination = (tablename, offset, limit, paginationContainer, fn) => {
    fetch(`/api/pagination/total/${tablename}`).then((res) => {
      if (res.status === 200){
        res.json().then(data => {
          total = data.result;
  
          if (total < limit){
            limit = total;
          }

          let itemsPerPage = limit - offset;
  
          let pageCount = total/itemsPerPage;
  
          let btns = Array(pageCount);
          
          for (let i = 0; i < pageCount; i++){
            btns.push(`
              <button 
              class="rounded-xl bg-turqoise text-white font-bold px-2 text-center"
              onclick="${fn}(${itemsPerPage*i})">
              ${i + 1}
              </button>
            `)
          }
          paginationContainer.innerHTML = btns.join('\n')
          //show pagination
          Promise.resolve('OK')
        })
      }
    });
  }
