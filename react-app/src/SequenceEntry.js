import { useState } from 'react';
import { useEffect } from 'react';
//var fetch = require('node-fetch');
import NodeFetch from 'node-fetch';

const SequenceEntry = () => {
    const [WT, setWT] = useState();
    const [SNP, setSNP] = useState();

    const sendUpdate = (data) => {
        //var data = {'WT': WT, 'SNP': SNP};

        NodeFetch('http://127.0.0.1:5000/send_input', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST',
		body: JSON.stringify(data)
        }).then(function (response) {
            return response.text();
        })
    }

    /*
    const handleWT = (event, newValue) => {
        setWT(newValue);
        sendUpdate();
    };

    const handleSNP = (event, newValue) => {
        setSNP(newValue);
        sendUpdate();
    };*/

    /*useEffect(() => {
        const interval2 = setInterval(() => {
            sendUpdate();
        }, 1000);
        return () => {
          clearInterval(interval2);
        };
      }, []);*/

    return (
        <div className="sequenceentry">
            <div class="seq-form" id="non-mut-form">
                <label for="non-mut">WT Sequence</label>
                <input type="text" value={WT} id="non-mut" name="non-mut" onChange={i => sendUpdate({'WT': i.target.value})} />
            </div>
            <div class="seq-form" id="mut-form">
                <label for="mut">Mutated Sequence</label>
                <input type="text" value={SNP} id="mut" name="mut" onChange={j => sendUpdate({'SNP': j.target.value})} />
            </div>
        </div>
    );
};

export default SequenceEntry;