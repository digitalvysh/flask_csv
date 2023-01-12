import React, { useState, useEffect } from 'react'

const Date = () => {
    const [d1, setD1] = useState("")
    const [d2, setD2] = useState("")
    const [data, setData] = useState([])

    const sync_data = async (d1, d2) => {
        const jsonData = await fetch(process.env.REACT_APP_API + "/date", {
            method: "POST",
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sd: d1,
                ed: d2
            }),
        });

        const response = await jsonData.json();
        setData(response)
        console.log(response);
    }

    useEffect(() => {
        if (d1.length && d2.length) {
            sync_data(d1, d2)
        }
    }, [d1, d2])

    return (
        <div>
            <div>
                <div>
                    Starting Date
                    <br />
                    <input type="date" name="date1" id="date1" value={d1} onChange={e => { setD1(e.target.value) }} />
                </div>
                <div>
                    Ending date
                    <br />
                    <input type="date" name="date2" id="date2" value={d2} onChange={e => { setD2(e.target.value) }} />
                </div>
            </div>
            <div>

                <table>
                    <thead>
                        <tr>
                            <th>image_name</th>
                            <th>objects_detected</th>
                            <th>image</th>
                        </tr>

                    </thead>
                    <tbody>
                        {data.map((e, idx) => (
                            <tr key={idx}>
                                <td>{e.image_name}</td>
                                <td>{e.objects_detected}</td>
                                <td><img src={`${process.env.REACT_APP_API}/data?img=${e.image_name}`} alt={e.image_name} /></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default Date