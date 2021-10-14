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
