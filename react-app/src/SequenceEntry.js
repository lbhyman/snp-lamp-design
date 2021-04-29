import { useState } from 'react';
//var fetch = require('node-fetch');
import NodeFetch from 'node-fetch';

const SequenceEntry = () => {
    const [WT, setWT] = useState();
    const [SNP, setSNP] = useState();

    const sendUpdate = () => {
        var data = {'WT': WT, 'SNP': SNP};

        NodeFetch('http://127.0.0.1:5000/send_input', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST',
		body: JSON.stringify(data)
        }).then(function (response) {
            return response.text();
        })
    }

    const handleWT = (event, newValue) => {
        setWT(newValue);
        sendUpdate();
    };

    const handleSNP = (event, newValue) => {
        setSNP(newValue);
        sendUpdate();
    };

    return (
        <div className="sequenceentry">
            <div class="seq-form" id="non-mut-form">
                <label for="non-mut">WT Sequence</label>
                <input type="text" id="non-mut" name="non-mut" onChange={handleWT} />
            </div>
            <div class="seq-form" id="mut-form">
                <label for="mut">Mutated Sequence</label>
                <input type="text" id="mut" name="mut" onChange={handleSNP} />
            </div>
        </div>
    );
};

export default SequenceEntry;