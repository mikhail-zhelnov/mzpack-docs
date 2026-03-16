import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/getting-started/installation">
            Get Started
          </Link>
          <Link
            className="button button--secondary button--outline button--lg"
            style={{marginLeft: '1rem'}}
            to="/api/getting-started/overview">
            API Reference
          </Link>
          <Link
            className="button button--secondary button--outline button--lg"
            style={{marginLeft: '1rem'}}
            href="https://discord.gg/ET8MBqW83d">
            Discord
          </Link>
          <Link
            className="button button--secondary button--outline button--lg"
            style={{marginLeft: '1rem'}}
            href="https://mzpack.freshdesk.com">
            Helpdesk
          </Link>
        </div>
      </div>
    </header>
  );
}

type FeatureItem = {
  title: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Order Flow Analysis',
    description: (
      <>
        Analyze real-time order flow with footprint charts, volume delta,
        and big trade detection. Understand market microstructure at every tick.
      </>
    ),
  },
  {
    title: 'Volume Profiling',
    description: (
      <>
        Identify key price levels with TPO profiles, POC, value area,
        and composite volume analysis across any timeframe.
      </>
    ),
  },
  {
    title: 'Algorithmic Trading',
    description: (
      <>
        Build automated strategies with the MZpack strategy pipeline.
        Entry, exit, trail, and filter components with built-in risk management.
      </>
    ),
  },
];

function Feature({title, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md" style={{paddingTop: '2rem'}}>
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home(): ReactNode {
  return (
    <Layout
      title="Documentation"
      description="MZpack documentation — order flow analysis and algorithmic trading for NinjaTrader 8">
      <HomepageHeader />
      <main>
        <section style={{display: 'flex', alignItems: 'center', padding: '2rem 0', width: '100%'}}>
          <div className="container">
            <div className="row">
              {FeatureList.map((props, idx) => (
                <Feature key={idx} {...props} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
