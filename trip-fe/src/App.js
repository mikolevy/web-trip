import React  from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import {map, tileLayer, polyline, circleMarker} from "leaflet";

function BusesList({ buses, onSelect, selectedBus }) {
    const busesInfo = [...buses]
    const busesRows = [];
    while(busesInfo.length) {

        const busesChunk = busesInfo.splice(0, 10)
        const busesRow = busesChunk.map((busInfo) => {
            return (
                <td
                    key={busInfo.number}
                    onClick={() => onSelect(busInfo.number)}
                    className={busInfo.number === selectedBus ? "bus-number-selected bus-number" : "bus-number"}
                >
                    {busInfo.number}
                </td>
            )
        });
        busesRows.push((
            <tr key={busesChunk[0].number}>
                {busesRow}
            </tr>
        ));
    }

    return (
        <table>
            <tbody>
                {busesRows}
            </tbody>
        </table>
    )
}

function TripForm({srcAddress, onSrcChange, dstAddress, onDstChange, searchTrip}) {

    return (
      <div className="current-order">

        Start: <input value={srcAddress} onChange={e => onSrcChange(e.target.value)}/><br/>
        Cel: <input value={dstAddress} onChange={e => onDstChange(e.target.value)}/>
        <div><button onClick={() => searchTrip()}>Wyszukaj</button></div>
      </div>
  );
}
const initialBuses = [
        {number: 2},
        {number: 5},
        {number: 8},
        {number: 101},
        {number: 102},
        {number: 105},
        {number: 108},
        {number: 125},
        {number: 127},
        {number: 155},
        {number: 158},
        {number: 250},
    ]

const initialTripProposal = {
    departureTime: "15:50",
    arrivalTime: "16:17",
    srcStop: "Zaspa",
    dstStop: "Główny",
    srcLocation: [54.3967, 18.59796],
    dstLocation: [54.37536, 18.6266],
    stops: [
        [54.3967, 18.59796],
        [54.39431, 18.60203],
        [54.39185, 18.6061],
        [54.38974, 18.6084],
        [54.38697, 18.61073],
        [54.3835, 18.61455],
        [54.3829, 18.62181],
        [54.3789, 18.62246],
        [54.37641, 18.62351],
        [54.37536, 18.6266],
    ]
}

var tripMap = null;

function renderMap(tripProposal) {
    const gdansLocation = [54.3782, 18.60874]
    tripMap = map('map').setView(gdansLocation, 12);

    tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(tripMap);

    if (tripProposal === null)
        return

    polyline(tripProposal.stops).addTo(tripMap);
    for(const stop of tripProposal.stops) {
        circleMarker(stop, {color: "blue"}).addTo(tripMap);
    }
    circleMarker(tripProposal.srcLocation, {color: "red"}).addTo(tripMap);
    circleMarker(tripProposal.dstLocation, {color: "green"}).addTo(tripMap);
}

export default function TripAssistance() {
    const [buses, setBuses] = useState([])
    const [selectedBus, setSelectedBus] = useState('')
    const [srcAddress, setSrcAddress] = useState('')
    const [dstAddress, setDstAddress] = useState('')
    const [tripProposal, setTripProposal] = useState(null)
    const [errors, setErrors] = useState('')

    const searchTrip = () => {

        axios
         .post('http://127.0.0.1:8000/trip-assistance-api/propose-trip', {
            src_address: srcAddress,
            dst_address: dstAddress,
            bus_number: selectedBus,
         })
         .then((response) => {
            setErrors('')
            setTripProposal(response.data);
            tripMap.remove()
            renderMap(tripProposal);
         })
         .catch((err) => {
            setTripProposal(null)
            setErrors("Nie znaleziono połączenia")
            console.log(err);
         });
    }

    useEffect(() => {
        if (tripMap)
            tripMap.remove()
        renderMap(tripProposal);
    }, [tripProposal])

    useEffect(() => {
      axios
         .get('http://127.0.0.1:8000/trip-assistance-api/bus-lines')
         .then((response) => {
            setBuses(response.data);
         })
         .catch((err) => {
            console.log(err);
            setBuses(initialBuses);
         });
   }, []);

    return (

        <div className={"container"}>
          <div>
          <p><b>Lista pojazdów</b></p>
            <BusesList buses={buses} onSelect={setSelectedBus} selectedBus={selectedBus}/>
          </div>
          <div className="order">
          <hr/><br/>
            <p><b>Gdzie chcesz jechać?</b></p>
            <TripForm
                srcAddress={srcAddress}
                onSrcChange={setSrcAddress}
                dstAddress={dstAddress}
                onDstChange={setDstAddress}
                searchTrip={searchTrip}
            />
          </div>
            <hr/>
            { tripProposal && (
                <div>
                    <p>Wyrusz o {tripProposal.departureTime} z przystanku {tripProposal.srcStop}</p>
                    <p>Jedź linią numer {selectedBus} do przystanku {tripProposal.dstStop}</p>
                    <p>Na miejscu będziesz o {tripProposal.arrivalTime}</p>
                    <hr/>
                </div>)
            }
            { errors && (
                <div>
                    <p>{errors}</p>
                </div>
            )}
            <div id={"map"} className={"map-container"} />
        </div>
      );
}