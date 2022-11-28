import { GithubLogo, Globe } from 'phosphor-react';

function About() {
  return (
    <div className="about">
      <div className="title">About Us</div>
      <div className="subtitle">
        This project was made as a part of the course <strong>Technology for Special Needs Education</strong> offered by
        the Centre for Educational Technology in the academic semester of Autumn 2022. The source code can be found{' '}
        <a href="https://github.com/chirag-ghosh/SpeakUp">here</a>. The contributors are
      </div>
      <div className="team">
        <div className="member">
          <div className="name">Sarita Singh</div>
          <div className="roll">(20CS10053)</div>
          <div className="links">
            <a href="https://github.com/sarita-singh">
              <GithubLogo size={40} />
            </a>
          </div>
        </div>
        <div className="member">
          <div className="name">Jatin Gupta</div>
          <div className="roll">(20CS10087)</div>
          <div className="links">
            <a href="https://github.com/jatin0101">
              <GithubLogo size={40} />
            </a>
          </div>
        </div>
        <div className="member">
          <div className="name">Nikhil Saraswat</div>
          <div className="roll">(20CS10039)</div>
          <div className="links">
            <a href="https://github.com/sarita-singh">
              <GithubLogo size={40} />
            </a>
          </div>
        </div>
        <div className="member">
          <div className="name">Amit Kumar</div>
          <div className="roll">(20CS30003)</div>
          <div className="links">
            <a href="https://github.com/sarita-singh">
              <GithubLogo size={40} />
            </a>
          </div>
        </div>
        <div className="member">
          <div className="name">Chirag Ghosh</div>
          <div className="roll">(20CS10020)</div>
          <div className="links">
            <a href="https://github.com/chirag-ghosh">
              <GithubLogo size={40} />
            </a>
            <a href="https://chiragghosh.dev">
              <Globe size={40} />
            </a>
          </div>
        </div>
        <div className="member">
          <div className="name">Manami Mondal</div>
          <div className="roll">(20CS10033)</div>
          <div className="links">
            <a href="https://github.com/chirag-ghosh">
              <GithubLogo size={40} />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;
