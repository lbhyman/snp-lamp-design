import Slider from '@material-ui/core/Slider';
import Typography from '@material-ui/core/Typography';
import { useState } from 'react';

function valuetext(value) {
    return `${2 ** value}`;
  }

const PopSlider = () => {
    const sliderMin = 16;
    const sliderMax = 4096;
    var sliderStart = 128;
    var sliderValue = sliderStart;
    const [value, setValue] = useState(Math.log2(sliderValue));
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <div className="popslider">
            <label for="population slider" className="sliderlabel">Starting Population: {2 ** value}</label>
            <Slider
                defaultValue={Math.log2(sliderValue)}
                getAriaValueText={valuetext}
                aria-labelledby="discrete-slider"
                valueLabelDisplay="auto"
                onChange={handleChange}
                step={1}
                marks
                scale={(x) => 2 ** x}
                min={Math.log2(sliderMin)}
                max={Math.log2(sliderMax)}
            />
        </div>
    );
};

export default PopSlider;