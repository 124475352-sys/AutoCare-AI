const make = document.getElementById("make");
const model = document.getElementById("model");
const year = document.getElementById("year");
const engine = document.getElementById("engine");

function populate(select, values) {
    select.innerHTML = "";

    [...new Set(values)].forEach(value => {
        select.add(new Option(value, value));
    });
}

function updateModels() {
    const filtered = vehicles.filter(
        v => v.make === make.value
    );

    populate(model, filtered.map(v => v.model));
    updateYears();
}

function updateYears() {
    const filtered = vehicles.filter(
        v => v.make === make.value &&
             v.model === model.value
    );

    populate(year, filtered.map(v => v.year));
    updateEngines();
}

function updateEngines() {
    const filtered = vehicles.filter(
        v => v.make === make.value &&
             v.model === model.value &&
             v.year === Number(year.value)
    );

    populate(engine, filtered.map(v => v.engine));
}

make.addEventListener("change", updateModels);
model.addEventListener("change", updateYears);
year.addEventListener("change", updateEngines);

populate(make, vehicles.map(v => v.make));
updateModels();