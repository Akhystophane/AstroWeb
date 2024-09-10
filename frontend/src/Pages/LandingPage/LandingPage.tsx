import HeroSection from './containers/HeroSection'
import BirthChartSection from './containers/BirthChartSection'
import HoroscopeSection from './containers/HoroscopeSection'
import FAQ from './containers/FAQ'
import StarsBackground from '../../assets/StarsBackground.svg'






function App() {

  return (
    <>

      <div className='h-full w-full' style={{ backgroundImage: `url(${StarsBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
        < HeroSection  />
        < BirthChartSection />
        < HoroscopeSection />
        < FAQ/>
      </div>

    </>
  )
}

export default App
