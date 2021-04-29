import SequenceEntry from './SequenceEntry';
import ConditionEntry from './ConditionEntry';
import PopSlider from './PopSlider';
import Buttons from './Buttons';
import Output from './Output';

function App() {
    return (
      <div className="App">
        <h1>SNP-LAMP Designer</h1>
        <SequenceEntry />
        <ConditionEntry />
        <PopSlider />
        <Buttons />
        <Output />
      </div>
    );

}

export default App;
