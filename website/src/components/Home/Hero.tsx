import React from "react";

import Link from "@docusaurus/Link";
import useBaseUrl from "@docusaurus/useBaseUrl";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useNonepressThemeConfig } from "@nullbot/docusaurus-theme-nonepress/client";

import Heading from "@theme/Heading";

function HomeHero(): React.ReactNode {
  const {
    siteConfig: { tagline },
  } = useDocusaurusContext();
  const {
    navbar: { logo },
  } = useNonepressThemeConfig();
  const logoSrc = useBaseUrl(logo!.src);

  return (
    <div className="home-hero">
      <img src={logoSrc} alt={logo!.alt} className="home-hero-logo" />
      <Heading as="h1" className="home-hero-title">
        <span className="text-primary">N</span>one
        <span className="text-primary">B</span>ot
      </Heading>
      <p className="home-hero-tagline">{tagline}</p>
      <div className="home-hero-actions">
        <Link to="/docs/guide/" className="btn btn-primary">
          开始使用 <FontAwesomeIcon icon={["fas", "chevron-right"]} />
        </Link>
      </div>
      <div className="home-hero-next">
        <FontAwesomeIcon icon={["fas", "angle-down"]} />
      </div>
    </div>
  );
}

export default React.memo(HomeHero);
