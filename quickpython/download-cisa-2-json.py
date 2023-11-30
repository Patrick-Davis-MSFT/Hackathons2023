# to run 
# import requirements
# pip install -r ./requirements.txt
# run the command
# python .\download-cisa-2-json.py -a 'https://www.cisa.gov/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&page=' -p 14 -b 'https://www.cisa.gov'


import pandas as pd
import argparse
from bs4 import BeautifulSoup
import re

html2 = """
<!DOCTYPE html>
<html lang="en" dir="ltr" prefix="og: https://ogp.me/ns#" class="no-js">
  <head>
    <meta charset="utf-8" />
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MDR73GM0K"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments)};gtag("js", new Date());gtag("set", "developer_id.dMDhkMT", true);gtag("config", "G-9MDR73GM0K", {"groups":"default","page_placeholder":"PLACEHOLDER_page_location"});</script>
<link rel="canonical" href="https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a" />
<meta property="og:site_name" content="Cybersecurity and Infrastructure Security Agency CISA" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a" />
<meta property="og:title" content="Publicly Available Tools Seen in Cyber Incidents Worldwide | CISA" />
<meta name="Generator" content="Drupal 10 (https://www.drupal.org)" />
<meta name="MobileOptimized" content="width" />
<meta name="HandheldFriendly" content="true" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" href="/profiles/cisad8_gov/themes/custom/gesso/favicon.png" type="image/png" />

    <title>Publicly Available Tools Seen in Cyber Incidents Worldwide | CISA</title>
    <link rel="stylesheet" media="all" href="/core/modules/system/css/components/ajax-progress.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/align.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/autocomplete-loading.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/fieldgroup.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/container-inline.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/clearfix.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/details.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/hidden.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/item-list.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/js.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/nowrap.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/position-container.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/progress.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/reset-appearance.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/resize.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/sticky-header.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/system-status-counter.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/system-status-report-counters.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/system-status-report-general-info.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/tabledrag.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/tablesort.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/tree-child.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/views/css/views.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/responsive_tables_filter/css/tablesaw-base.css?s4w5q2" />
<link rel="stylesheet" media="screen" href="/modules/contrib/responsive_tables_filter/css/tablesaw-responsive.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/responsive_tables_filter/css/tables.columntoggle.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/responsive_tables_filter/css/customizations.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/profiles/cisad8_gov/modules/custom/toolbar_tasks/css/toolbar.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/extlink/extlink.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/profiles/cisad8_gov/modules/custom/cisa_core/css/ckeditor-expandabletextbox.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/ckeditor_accordion/css/accordion.frontend.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/better_social_sharing_buttons/css/better_social_sharing_buttons.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/paragraphs/css/paragraphs.unpublished.css?s4w5q2" />
<link rel="stylesheet" media="all" href="//fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;family=Public+Sans:wght@400;500;600;700&amp;display=swap" />
<link rel="stylesheet" media="all" href="/profiles/cisad8_gov/themes/custom/gesso/dist/css/styles.css?s4w5q2" />

    
  </head>
  <body  class="path-node not-front node-page node-page--node-type-advisory" id="top">
    
<div  class="c-skiplinks">
  <a href="#main" class="c-skiplinks__link u-visually-hidden u-focusable">Skip to main content</a>
</div>
    
      <div class="dialog-off-canvas-main-canvas" data-off-canvas-main-canvas>
    

<div  class="l-site-container">
    
      
<section  class="usa-banner" aria-label="Official government website">
  <div class="usa-accordion">  <header class="usa-banner__header">
    <div class="usa-banner__inner">
      <div class="grid-col-auto">
        <img class="usa-banner__header-flag" src="/profiles/cisad8_gov/themes/custom/gesso/dist/images/us_flag_small.png" alt="U.S. flag" />
      </div>
      <div class="grid-col-fill tablet:grid-col-auto">
        <p class="usa-banner__header-text">An official website of the United States government</p>
              <p class="usa-banner__header-action" aria-hidden="true">Here’s how you know</p></div>
        <button class="usa-accordion__button usa-banner__button" aria-expanded="false" aria-controls="gov-banner">
          <span class="usa-banner__button-text">Here’s how you know</span>
        </button>
          </div>
  </header>
      <div class="usa-banner__content usa-accordion__content" id="gov-banner">
      <div class="grid-row grid-gap-lg">
                  <div class="usa-banner__guidance tablet:grid-col-6">
            <img class="usa-banner__icon usa-media-block__img" src="/profiles/cisad8_gov/themes/custom/gesso/dist/images/icon-dot-gov.svg" alt="Dot gov">
            <div class="usa-media-block__body">
              <p>
                <strong>Official websites use .gov</strong>
                <br> A <strong>.gov</strong> website belongs to an official government organization in the United States.
              </p>
            </div>
          </div>
                  <div class="usa-banner__guidance tablet:grid-col-6">
            <img class="usa-banner__icon usa-media-block__img" src="/profiles/cisad8_gov/themes/custom/gesso/dist/images/icon-https.svg" alt="HTTPS">
            <div class="usa-media-block__body">
              <p>
                <strong>Secure .gov websites use HTTPS</strong>
                <br> A <strong>lock</strong> (<span class="icon-lock"><svg xmlns="http://www.w3.org/2000/svg" width="52" height="64" viewBox="0 0 52 64" class="usa-banner__lock-image" role="img" aria-labelledby="banner-lock-title banner-lock-description"><title id="banner-lock-title">Lock</title><desc id="banner-lock-description">A locked padlock</desc><path fill="#000000" fill-rule="evenodd" d="M26 0c10.493 0 19 8.507 19 19v9h3a4 4 0 0 1 4 4v28a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V32a4 4 0 0 1 4-4h3v-9C7 8.507 15.507 0 26 0zm0 8c-5.979 0-10.843 4.77-10.996 10.712L15 19v9h22v-9c0-6.075-4.925-11-11-11z"/></svg></span>) or <strong>https://</strong> means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.
              </p>
            </div>
          </div>
              </div>
    </div>
  </div>
  </section>

  
  


<div class="usa-overlay"></div>
<header  class="usa-header usa-header--extended" role="banner">
        
<div  class="usa-navbar">
  <div class="l-constrain">
    <div class="usa-navbar__row">
      <div class="usa-navbar__brand">
        
<a  class="c-site-name" href="/" rel="home" title="Go to the Cybersecurity & Infrastructure Security Agency homepage">
  <span class="c-site-name__text">Cybersecurity &amp; Infrastructure Security Agency</span>
</a>        <div class="usa-navbar__tagline">America's Cyber Defense Agency</div>
      </div>
      <div class="usa-navbar__search">
        <div class="usa-navbar__search-header">
          <p>Search</p>
        </div>
        
<div  class="usa-search">
  <script async src=https://cse.google.com/cse.js?cx=ffc4c79e29d5b3a8c></script>
  <div class="gcse-searchbox-only" data-resultsurl="/search">&nbsp;</div>
</div>
      </div>
      <button class="mobile-menu-button usa-menu-btn">Menu</button>
    </div>
  </div>
</div>
    

<nav  class="usa-nav" role="navigation" aria-label="Primary navigation">
  <div class="usa-nav__inner l-constrain">
    <div class="usa-nav__row">
      <button class="usa-nav__close">Close</button>
      
<div  class="usa-search">
  <script async src=https://cse.google.com/cse.js?cx=ffc4c79e29d5b3a8c></script>
  <div class="gcse-searchbox-only" data-resultsurl="/search">&nbsp;</div>
</div>
                
  
          <ul class="usa-nav__primary usa-accordion">
    
    
              <li class="usa-nav__primary-item topics">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-1">
          <span>Topics</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-1" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/topics">Topics</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/cybersecurity-best-practices">
          <span>Cybersecurity Best Practices</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/cyber-threats-and-advisories">
          <span>Cyber Threats and Advisories</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/critical-infrastructure-security-and-resilience">
          <span>Critical Infrastructure Security and Resilience</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/election-security">
          <span>Election Security</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/emergency-communications">
          <span>Emergency Communications</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/industrial-control-systems">
          <span>Industrial Control Systems</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/information-communications-technology-supply-chain-security">
          <span>Information and Communications Technology Supply Chain Security</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/partnerships-and-collaboration">
          <span>Partnerships and Collaboration</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/physical-security">
          <span>Physical Security</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/risk-management">
          <span>Risk Management</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          

<div  class="c-menu-feature-links">
      <div class="c-menu-feature-links__title">
      <a href="/audiences">        How can we help?
      </a>    </div>
        <div class="c-menu-feature-links__content"><a href="/topics/government">Government</a><a href="/topics/educational-institutions">Educational Institutions</a><a href="/topics/industry">Industry</a><a href="/topics/state-local-tribal-and-territorial">State, Local, Tribal, and Territorial</a><a href="/topics/individuals-and-families">Individuals and Families</a><a href="/topics/small-and-medium-businesses">Small and Medium Businesses</a><a href="/audiences/find-help-locally">Find Help Locally</a><a href="/audiences/faith-based-community">Faith-Based Community</a><a href="/audiences/executives">Executives</a></div>
  </div>

              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item spotlight">
      
      
                      <a href="/spotlight" class="usa-nav__link" >
          <span>Spotlight</span>
        </a>
              
              </li>
          
              <li class="usa-nav__primary-item resources--tools">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-3">
          <span>Resources &amp; Tools</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-3" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/resources-tools">Resources &amp; Tools</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/all-resources-tools">
          <span>All Resources &amp; Tools</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/services">
          <span>Services</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/programs">
          <span>Programs</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/resources">
          <span>Resources</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/training">
          <span>Training</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/groups">
          <span>Groups</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item news--events">
      
              <button class="usa-accordion__button usa-nav__link usa-current" aria-expanded="false" aria-controls="basic-mega-nav-section-4">
          <span>News &amp; Events</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-4" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/news-events">News &amp; Events</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/news">
          <span>News</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/events">
          <span>Events</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/cybersecurity-advisories">
          <span>Cybersecurity Alerts &amp; Advisories</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/directives">
          <span>Directives</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/request-speaker">
          <span>Request a CISA Speaker</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/congressional-testimony">
          <span>Congressional Testimony</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item careers">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-5">
          <span>Careers</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-5" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/careers">Careers</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/benefits-perks">
          <span>Benefits &amp; Perks</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/hirevue-applicant-reasonable-accommodations-process">
          <span>HireVue Applicant Reasonable Accommodations Process</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/general-recruitment-and-hiring-faqs">
          <span>Hiring</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/resume-application-tips">
          <span>Resume &amp; Application Tips</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/students-recent-graduates-employment-opportunities">
          <span>Students &amp; Recent Graduates</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/veteran-and-military-spouse-employment-opportunities">
          <span>Veteran and Military Spouses</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/work-cisa">
          <span>Work @ CISA</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item about">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-6">
          <span>About</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-6" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/about">About</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/culture">
          <span>Culture</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/divisions-offices">
          <span>Divisions &amp; Offices</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/regions">
          <span>Regions</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/leadership">
          <span>Leadership</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/doing-business-cisa">
          <span>Doing Business with CISA</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/site-links">
          <span>Site Links</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/reporting-employee-and-contractor-misconduct">
          <span>Reporting Employee and Contractor Misconduct</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/cisa-github">
          <span>CISA GitHub</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/contact-us">
          <span>Contact Us </span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
    
      </ul>
    
  


                    <a href="/report" class="c-button c-button--report">Report a Cyber Issue</a>
          </div>
  </div>
</nav>
    </header>


  <div class="gesso-mobile-tagline-container">
    <div class="usa-navbar__tagline">America's Cyber Defense Agency</div>
  </div>

  
  
<div  class="l-breadcrumb">
  <div class="l-constrain">
    <div class="l-breadcrumb__row">
      







  
  
    

  
              


<nav  aria-labelledby="breadcrumb-label" class="c-breadcrumb" role="navigation">
  <div class="l-constrain">
    <div
       id="breadcrumb-label" class="c-breadcrumb__title  u-visually-hidden">Breadcrumb</div>
    <ol class="c-breadcrumb__list">
              <li class="c-breadcrumb__item">
                      <a class="c-breadcrumb__link" href="/">Home</a>
                  </li>
              <li class="c-breadcrumb__item">
                      <a class="c-breadcrumb__link" href="/news-events">News & Events</a>
                  </li>
              <li class="c-breadcrumb__item">
                      <a class="c-breadcrumb__link" href="/news-events/cybersecurity-advisories">Cybersecurity Advisories</a>
                  </li>
              <li class="c-breadcrumb__item">
                      <a class="c-breadcrumb__link" href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94">Cybersecurity Advisory</a>
                  </li>
          </ol>
  </div>
</nav>

  
  
  
  






  <div  id="block-bettersocialsharingbuttons" class="c-block c-block--social-share c-block--provider-better-social-sharing-buttons c-block--id-social-sharing-buttons-block">

  
  
    

      <div  class="c-block__content">
  
      <div class="c-block__row">
      <span>Share:</span>
      

<div style="display: none"><link rel="preload" href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg" as="image" type="image/svg+xml" crossorigin="anonymous" /></div>

<div class="social-sharing-buttons">
                <a href="https://www.facebook.com/sharer/sharer.php?u=https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a&amp;title=Publicly%20Available%20Tools%20Seen%20in%20Cyber%20Incidents%20Worldwide" target="_blank" title="Share to Facebook" aria-label="Share to Facebook" class="social-sharing-buttons__button share-facebook" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#facebook" />
            </svg>
        </a>
    
                <a href="https://twitter.com/intent/tweet?text=Publicly%20Available%20Tools%20Seen%20in%20Cyber%20Incidents%20Worldwide+https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a" target="_blank" title="Share to Twitter" aria-label="Share to Twitter" class="social-sharing-buttons__button share-twitter" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#twitter" />
            </svg>
        </a>
    
        
        
        
                <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a" target="_blank" title="Share to Linkedin" aria-label="Share to Linkedin" class="social-sharing-buttons__button share-linkedin" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#linkedin" />
            </svg>
        </a>
    
        
        
        
        
        
                <a href="mailto:?subject=Publicly%20Available%20Tools%20Seen%20in%20Cyber%20Incidents%20Worldwide&amp;body=https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a" title="Share to Email" aria-label="Share to Email" class="social-sharing-buttons__button share-email" target="_blank" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#email" />
            </svg>
        </a>
    
        
    </div>

    </div>
  
      </div>
  
  
  </div>

    </div>
  </div>
</div>

  
  

  <main id="main" class="c-main" role="main" tabindex="-1">
    
      
    


<div  class="l-content">
          







  
  
    

  
            





<div  class="is-promoted l-full">
    <div class="l-full__header">
        
<div  class="c-page-title">
  <div class="c-page-title__inner l-constrain">
    <div class="c-page-title__row">
      <div class="c-page-title__content">
                  <div class="c-page-title__meta">Cybersecurity Advisory</div>
                <h1 class="c-page-title__title">
<span>Publicly Available Tools Seen in Cyber Incidents Worldwide</span>
</h1>
                                                          <div class="c-page-title__fields">  




<div  class="c-field c-field--name-field-last-updated c-field--type-datetime c-field--label-above">
  <div  class="c-field__label">Last Revised</div><div class="c-field__content"><time datetime="2020-06-30T12:00:00Z">June 30, 2020</time></div></div>

  




<div  class="c-field c-field--name-field-alert-code c-field--type-string c-field--label-above">
  <div  class="c-field__label">Alert Code</div><div class="c-field__content">AA18-284A</div></div>

</div>
                        
        
      </div>
          </div>
    <div class="c-page-title__decoration"></div>
  </div>
</div>
    </div>
    <div class="l-full__main">
                      

<div  class="l-page-section l-page-section--rich-text">
      <div class="l-constrain">
  
  
  <div class="l-page-section__content">
          <div>
<h3>Summary</h3>
</div>
<p>This report is a collaborative research effort by the cyber security authorities of five nations: Australia, Canada, New Zealand, the United Kingdom, and the United States.<a href="https://www.acsc.gov.au/">[1]</a><a href="https://cyber.gc.ca/en/">[2]</a><a href="https://www.ncsc.govt.nz/">[3]</a><a href="https://www.ncsc.gov.uk/">[4]</a><a href="/">[5]</a></p>
<p>In it we highlight the use of five publicly available tools, which have been used for malicious purposes in recent cyber incidents around the world. The five tools are:</p>
<ol><li><a href="#Remote%20Access%20Trojan:%20JBiFrost">Remote Access Trojan: JBiFrost</a></li>
<li><a href="#Webshell:%20China%20Chopper">Webshell: China Chopper</a></li>
<li><a href="#Credential%20Stealer:%20Mimikatz">Credential Stealer: Mimikatz</a></li>
<li><a href="#Lateral%20Movement%20Framework:%20PowerShell%20Empire">Lateral Movement Framework: PowerShell Empire</a></li>
<li><a href="#C2%20Obfuscation%20and%20Exfiltration:%20HUC%20Packet%20Transmitter">C2 Obfuscation and Exfiltration: HUC Packet Transmitter</a></li>
</ol><p>To aid the work of network defenders and systems administrators, we also provide advice on limiting the effectiveness of these tools and detecting their use on a network.</p>
<p>The individual tools we cover in this report are limited examples of the types of tools used by threat actors. You should not consider this an exhaustive list when planning your network defense.</p>
<p>Tools and techniques for exploiting networks and the data they hold are by no means the preserve of nation states or criminals on the dark web. Today, malicious tools with a variety of functions are widely and freely available for use by everyone from skilled penetration testers, hostile state actors and organized criminals, to amateur cyber criminals.</p>
<p>The tools in this Activity Alert have been used to compromise information across a wide range of critical sectors, including health, finance, government, and defense. Their widespread availability presents a challenge for network defense and threat-actor attribution.</p>
<p>Experience from all our countries makes it clear that, while cyber threat actors continue to develop their capabilities, they still make use of established tools and techniques. Even the most sophisticated threat actor groups use common, publicly available tools to achieve their objectives.</p>
<p>Whatever these objectives may be, initial compromises of victim systems are often established through exploitation of common security weaknesses. Abuse of unpatched software vulnerabilities or poorly configured systems are common ways for a threat actor to gain access. The tools detailed in this Activity Alert come into play once a compromise has been achieved, enabling attackers to further their objectives within the victim’s systems.</p>
<h4>How to Use This Report</h4>
<p>The tools detailed in this Activity Alert fall into five categories: Remote Access Trojans (RATs), webshells, credential stealers, lateral movement frameworks, and command and control (C2) obfuscators.</p>
<p>This Activity Alert provides an overview of the threat posed by each tool, along with insight into where and when it has been deployed by threat actors. Measures to aid detection and limit the effectiveness of each tool are also described.</p>
<p>The Activity Alert concludes with general advice for improving network defense practices.</p>
<div>
<h3>Technical Details</h3>
</div>
<h4><a id=" JBiFrost">Remote Access Trojan: JBiFrost</a> </h4>
<p>First observed in May 2015, the JBiFrost RAT is a variant of the Adwind RAT, with roots stretching back to the Frutas RAT from 2012.</p>
<p>A RAT is a program that, once installed on a victim’s machine, allows remote administrative control. In a malicious context, it can—among many other functions—be used to install backdoors and key loggers, take screen shots, and exfiltrate data.</p>
<p>Malicious RATs can be difficult to detect because they are normally designed not to appear in lists of running programs and can mimic the behavior of legitimate applications.</p>
<p>To prevent forensic analysis, RATs have been known to disable security measures (e.g., Task Manager) and network analysis tools (e.g., Wireshark) on the victim’s system.</p>
<h5>In Use</h5>
<p>JBiFrost RAT is typically employed by cyber criminals and low-skilled threat actors, but its capabilities could easily be adapted for use by state-sponsored threat actors.</p>
<p>Other RATs are widely used by Advanced Persistent Threat (APT) actor groups, such as Adwind RAT, against the aerospace and defense sector; or Quasar RAT, by APT10, against a broad range of sectors.</p>
<p>Threat actors have repeatedly compromised servers in our countries with the purpose of delivering malicious RATs to victims, either to gain remote access for further exploitation, or to steal valuable information such as banking credentials, intellectual property, or PII.</p>
<h5>Capabilities</h5>
<p>JBiFrost RAT is Java-based, cross-platform, and multifunctional. It poses a threat to several different operating systems, including Windows, Linux, MAC OS X, and Android.</p>
<p>JBiFrost RAT allows threat actors to pivot and move laterally across a network or install additional malicious software. It is primarily delivered through emails as an attachment, usually an invoice notice, request for quotation, remittance notice, shipment notification, payment notice, or with a link to a file hosting service.</p>
<p>Past infections have exfiltrated intellectual property, banking credentials, and personally identifiable information (PII). Machines infected with JBiFrost RAT can also be used in botnets to carry out distributed denial-of-service attacks.</p>
<h5>Examples</h5>
<p>Since early 2018, we have observed an increase in JBiFrost RAT being used in targeted attacks against critical national infrastructure owners and their supply chain operators. There has also been an increase in the RAT’s hosting on infrastructure located in our countries.</p>
<p>In early 2017, Adwind RAT was deployed via spoofed emails designed to look as if they originated from Society for Worldwide Interbank Financial Telecommunication, or SWIFT, network services.</p>
<p>Many other publicly available RATs, including variations of Gh0st RAT, have also been observed in use against a range of victims worldwide.</p>
<h5>Detection and Protection</h5>
<p>Some possible indications of a JBiFrost RAT infection can include, but are not limited to:</p>
<ul><li>Inability to restart the computer in safe mode,</li>
<li>Inability to open the Windows Registry Editor or Task Manager,</li>
<li>Significant increase in disk activity and/or network traffic,</li>
<li>Connection attempts to known malicious Internet Protocol (IP) addresses, and</li>
<li>Creation of new files and directories with obfuscated or random names.</li>
</ul><p>Protection is best afforded by ensuring systems and installed applications are all fully patched and updated. The use of a modern antivirus program with automatic definition updates and regular system scans will also help ensure that most of the latest variants are stopped in their tracks. You should ensure that your organization is able to collect antivirus detections centrally across its estate and investigate RAT detections efficiently.</p>
<p>Strict application allow listing is recommended to prevent infections from occurring.</p>
<p>The initial infection mechanism for RATs, including JBiFrost RAT, can be via phishing emails. You can help prevent JBiFrost RAT infections by stopping these phishing emails from reaching your users, helping users to identify and report phishing emails, and implementing security controls so that the malicious email does not compromise your device. The United Kingdom National Cyber Security Centre (UK NCSC) has published <a href="https://www.ncsc.gov.uk/phishing">phishing guidance</a>.</p>
<h4><a id=" China Chopper">Webshell: China Chopper</a> </h4>
<p>China Chopper is a publicly available, well-documented webshell that has been in widespread use since 2012.</p>
<p>Webshells are malicious scripts that are uploaded to a target host after an initial compromise and grant a threat actor remote administrative capability.</p>
<p>Once this access is established, webshells can also be used to pivot to additional hosts within a network.</p>
<h5>In Use</h5>
<p>China Chopper is extensively used by threat actors to remotely access compromised web servers, where it provides file and directory management, along with access to a virtual terminal on the compromised device.</p>
<p>As China Chopper is just 4 KB in size and has an easily modifiable payload, detection and mitigation are difficult for network defenders.</p>
<h5>Capabilities</h5>
<p>China Chopper has two main components: the China Chopper client-side, which is run by the attacker, and the China Chopper server, which is installed on the victim web server but is also attacker-controlled.</p>
<p>The webshell client can issue terminal commands and manage files on the victim server. Its MD5 hash is publicly available (originally posted on hxxp://www.maicaidao.com).</p>
<p>The MD5 hash of the web client is shown in table 1 below.</p>
<p><strong>Table 1: China Chopper webshell client MD5 hash</strong></p>
<table class="general-table tablesaw tablesaw-stack" data-tablesaw-mode="stack" data-tablesaw-minimap=""><thead><tr><th scope="col" role="columnheader" data-tablesaw-priority="persist"><strong>Webshell Client</strong></th>
<th scope="col" role="columnheader"><strong>MD5 Hash</strong></th>
</tr><tr><td>caidao.exe</td>
<td>5001ef50c7e869253a7c152a638eab8a</td>
</tr></thead></table><p>The webshell server is uploaded in plain text and can easily be changed by the attacker. This makes it harder to define a specific hash that can identify adversary activity. In summer 2018, threat actors were observed targeting public-facing web servers that were vulnerable to CVE-2017-3066. The activity was related to a vulnerability in the web application development platform Adobe ColdFusion, which enabled remote code execution.</p>
<p>China Chopper was intended as the second-stage payload, delivered once servers had been compromised, allowing the threat actor remote access to the victim host. After successful exploitation of a vulnerability on the victim machine, the text-based China Chopper is placed on the victim web server. Once uploaded, the webshell server can be accessed by the threat actor at any time using the client application. Once successfully connected, the threat actor proceeds to manipulate files and data on the web server.</p>
<p>China Chopper’s capabilities include uploading and downloading files to and from the victim using the file-retrieval tool <code>wget</code> to download files from the internet to the target; and editing, deleting, copying, renaming, and even changing the timestamp, of existing files.</p>
<h5>Detection and protection</h5>
<p>The most powerful defense against a webshell is to avoid the web server being compromised in the first place. Ensure that all the software running on public-facing web servers is up-to-date with security patches applied. Audit custom applications for common web vulnerabilities.<a href="https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project">[6]</a></p>
<p>One attribute of China Chopper is that every action generates a hypertext transfer protocol (HTTP) POST. This can be noisy and is easily spotted if investigated by a network defender.</p>
<p>While the China Chopper webshell server upload is plain text, commands issued by the client are Base64 encoded, although this is easily decodable.</p>
<p>The adoption of Transport Layer Security (TLS) by web servers has resulted in web server traffic becoming encrypted, making detection of China Chopper activity using network-based tools more challenging.</p>
<p>The most effective way to detect and mitigate China Chopper is on the host itself—specifically on public-facing web servers. There are simple ways to search for the presence of the web-shell using the command line on both Linux and Windows based operating systems.<a href="http://www.fireeye.com/blog/threat-research/2013/08/breaking-down-the-china-chopper-web-shell-part-ii.html">[7]</a></p>
<p>To detect webshells more broadly, network defenders should focus on spotting either suspicious process execution on web servers (e.g., Hypertext Preprocessor [PHP] binaries spawning processes) and out-of-pattern outbound network connections from web servers. Typically, web servers make predictable connections to an internal network. Changes in those patterns may indicate the presence of a web shell. You can manage network permissions to prevent web-server processes from writing to directories where PHP can be executed, or from modifying existing files.</p>
<p>We also recommend that you use web access logs as a source of monitoring, such as through traffic analytics. Unexpected pages or changes in traffic patterns can be early indicators.</p>
<h4><a id=" Mimikatz">Credential Stealer: Mimikatz</a> </h4>
<p>Developed in 2007, Mimikatz is mainly used by attackers to collect the credentials of other users, who are logged into a targeted Windows machine. It does this by accessing the credentials in memory within a Windows process called Local Security Authority Subsystem Service (LSASS).</p>
<p>These credentials, either in plain text, or in hashed form, can be reused to give access to other machines on a network.</p>
<p>Although it was not originally intended as a hacking tool, in recent years Mimikatz has been used by multiple actors for malicious purposes. Its use in compromises around the world has prompted organizations globally to re-evaluate their network defenses.</p>
<p>Mimikatz is typically used by threat actors once access has been gained to a host and the threat actor wishes to move throughout the internal network. Its use can significantly undermine poorly configured network security.</p>
<h5>In Use</h5>
<p>Mimikatz source code is publicly available, which means anyone can compile their own versions of the new tool and potentially develop new Mimikatz custom plug-ins and additional functionality.</p>
<p>Our cyber authorities have observed widespread use of Mimikatz among threat actors, including organized crime and state-sponsored groups.</p>
<p>Once a threat actor has gained local administrator privileges on a host, Mimikatz provides the ability to obtain the hashes and clear-text credentials of other users, enabling the threat actor to escalate privileges within a domain and perform many other post-exploitation and lateral movement tasks.</p>
<p>For this reason, Mimikatz has been bundled into other penetration testing and exploitation suites, such as PowerShell Empire and Metasploit.</p>
<h5>Capabilities</h5>
<p>Mimikatz is best known for its ability to retrieve clear text credentials and hashes from memory, but its full suite of capabilities is extensive.</p>
<p>The tool can obtain Local Area Network Manager and NT LAN Manager hashes, certificates, and long-term keys on Windows XP (2003) through Windows 8.1 (2012r2). In addition, it can perform pass-the-hash or pass-the-ticket tasks and build Kerberos “golden tickets.”</p>
<p>Many features of Mimikatz can be automated with scripts, such as PowerShell, allowing a threat actor to rapidly exploit and traverse a compromised network. Furthermore, when operating in memory through the freely available “Invoke-Mimikatz” PowerShell script, Mimikatz activity is very difficult to isolate and identify.</p>
<h5>Examples</h5>
<p>Mimikatz has been used across multiple incidents by a broad range of threat actors for several years. In 2011, it was used by unknown threat actors to obtain administrator credentials from the Dutch certificate authority, DigiNotar. The rapid loss of trust in DigiNotar led to the company filing for bankruptcy within a month of this compromise.</p>
<p>More recently, Mimikatz was used in conjunction with other malicious tools—in the NotPetya and BadRabbit ransomware attacks in 2017 to extract administrator credentials held on thousands of computers. These credentials were used to facilitate lateral movement and enabled the ransomware to propagate throughout networks, encrypting the hard drives of numerous systems where these credentials were valid.</p>
<p>In addition, a Microsoft research team identified use of Mimikatz during a sophisticated cyberattack targeting several high-profile technology and financial organizations. In combination with several other tools and exploited vulnerabilities, Mimikatz was used to dump and likely reuse system hashes.</p>
<h5>Detection and Protection</h5>
<p>Updating Windows will help reduce the information available to a threat actor from the Mimikatz tool, as Microsoft seeks to improve the protection offered in each new Windows version.</p>
<p>To prevent Mimikatz credential retrieval, network defenders should disable the storage of clear text passwords in LSASS memory. This is default behavior for Windows 8.1/Server 2012 R2 and later, but can be specified on older systems which have the relevant security patches installed.<a href="https://support.microsoft.com/en-us/help/2871997/microsoft-security-advisory-update-to-improve-credentials-protection-a">[8]</a> Windows 10 and Windows Server 2016 systems can be protected by using newer security features, such as Credential Guard.</p>
<p>Credential Guard will be enabled by default if:</p>
<ul><li>The hardware meets Microsoft’s Windows Hardware Compatibility Program Specifications and Policies for Windows Server 2016 and Windows Server Semi-Annual Branch; and</li>
<li>The server is not acting as a Domain Controller.</li>
</ul><p>You should verify that your physical and virtualized servers meet Microsoft’s <a href="https://docs.microsoft.com/en-us/windows/security/identity-protection/credential-guard/credential-guard-requirements">minimum requirements for each release of Windows 10 and Windows Server</a>.</p>
<p>Password reuse across accounts, particularly administrator accounts, makes pass-the-hash attacks far simpler. You should set user policies within your organization that discourage password reuse, even across common level accounts on a network. The freely available Local Administrator Password Solution from Microsoft can allow easy management of local administrator passwords, preventing the need to set and store passwords manually.</p>
<p>Network administrators should monitor and respond to unusual or unauthorized account creation or authentication to prevent Kerberos ticket exploitation, or network persistence and lateral movement. For Windows, tools such as Microsoft Advanced Threat Analytics and Azure Advanced Threat Protection can help with this.</p>
<p>Network administrators should ensure that systems are patched and up-to-date. Numerous Mimikatz features are mitigated or significantly restricted by the latest system versions and updates. But no update is a perfect fix, as Mimikatz is continually evolving and new third-party modules are often developed.</p>
<p>Most up-to-date antivirus tools will detect and isolate non-customized Mimikatz use and should therefore be used to detect these instances. But threat actors can sometimes circumvent antivirus systems by running Mimikatz in memory, or by slightly modifying the original code of the tool. Wherever Mimikatz is detected, you should perform a rigorous investigation, as it almost certainly indicates a threat actor is actively present in the network, rather than an automated process at work.</p>
<p>Several of Mimikatz’s features rely on exploitation of administrator accounts. Therefore, you should ensure that administrator accounts are issued on an as-required basis only. Where administrative access is required, you should apply privileged access management principles.</p>
<p>Since Mimikatz can only capture the accounts of those users logged into a compromised machine, privileged users (e.g., domain administrators) should avoid logging into machines with their privileged credentials. Detailed information on securing Active Directory is available from Microsoft.<a href="https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory">[9]</a></p>
<p>Network defenders should audit the use of scripts, particularly PowerShell, and inspect logs to identify anomalies. This will aid in identifying Mimikatz or pass-the-hash abuse, as well as in providing some mitigation against attempts to bypass detection software.</p>
<h4><a id=" PowerShell Empire">Lateral Movement Framework: PowerShell Empire</a> </h4>
<p>PowerShell Empire is an example of a post-exploitation or lateral movement tool. It is designed to allow an attacker (or penetration tester) to move around a network after gaining initial access. Other examples of these tools include Cobalt Strike and Metasploit. PowerShell Empire can also be used to generate malicious documents and executables for social engineering access to networks.</p>
<p>The PowerShell Empire framework was designed as a legitimate penetration testing tool in 2015. PowerShell Empire acts as a framework for continued exploitation once a threat actor has gained access to a system.</p>
<p>The tool provides a threat actor with the ability to escalate privileges, harvest credentials, exfiltrate information, and move laterally across a network. These capabilities make it a powerful exploitation tool. Because it is built on a common legitimate application (PowerShell) and can operate almost entirely in memory, PowerShell Empire can be difficult to detect on a network using traditional antivirus tools.</p>
<h5>In Use</h5>
<p>PowerShell Empire has become increasingly popular among hostile state actors and organized criminals. In recent years we have seen it used in cyber incidents globally across a wide range of sectors.</p>
<p>Initial exploitation methods vary between compromises, and threat actors can configure the PowerShell Empire uniquely for each scenario and target. This, in combination with the wide range of skill and intent within the PowerShell Empire user community, means that the ease of detection will vary. Nonetheless, having a greater understanding and awareness of this tool is a step forward in defending against its use by threat actors.</p>
<h5>Capabilities</h5>
<p>PowerShell Empire enables a threat actor to carry out a range of actions on a victim’s machine and implements the ability to run PowerShell scripts without needing powershell.exe to be present on the system Its communications are encrypted and its architecture is flexible.</p>
<p>PowerShell Empire uses "modules" to perform more specific malicious actions. These modules provide the threat actor with a customizable range of options to pursue their goals on the victim’s systems. These goals include escalation of privileges, credential harvesting, host enumeration, keylogging, and the ability to move laterally across a network.</p>
<p>PowerShell Empire’s ease of use, flexible configuration, and ability to evade detection make it a popular choice for threat actors of varying abilities.</p>
<h5>Examples</h5>
<p>During an incident in February 2018, a UK energy sector company was compromised by an unknown threat actor. This compromise was detected through PowerShell Empire beaconing activity using the tool’s default profile settings. Weak credentials on one of the victim’s administrator accounts are believed to have provided the threat actor with initial access to the network.</p>
<p>In early 2018, an unknown threat actor used Winter Olympics-themed socially engineered emails and malicious attachments in a spear-phishing campaign targeting several South Korean organizations. This attack had an additional layer of sophistication, making use of <code>Invoke-PSImage</code>, a stenographic tool that will encode any PowerShell script into an image.</p>
<p>In December 2017, APT19 targeted a multinational law firm with a phishing campaign. APT19 used obfuscated PowerShell macros embedded within Microsoft Word documents generated by PowerShell Empire.</p>
<p>Our cybersecurity authorities are also aware of PowerShell Empire being used to target academia. In one reported instance, a threat actor attempted to use PowerShell Empire to gain persistence using a Windows Management Instrumentation event consumer. However, in this instance, the PowerShell Empire agent was unsuccessful in establishing network connections due to the HTTP connections being blocked by a local security appliance.</p>
<h5>Detection and Protection</h5>
<p>Identifying malicious PowerShell activity can be difficult due to the prevalence of legitimate PowerShell activity on hosts and the increased use of PowerShell in maintaining a corporate environment.</p>
<p>To identify potentially malicious scripts, PowerShell activity should be comprehensively logged. This should include script block logging and PowerShell transcripts.</p>
<p>Older versions of PowerShell should be removed from environments to ensure that they cannot be used to circumvent additional logging and controls added in more recent versions of PowerShell. This page provides a good summary of PowerShell security practices.<a href="https://www.digitalshadows.com/blog-and-research/powershell-security-best-practices/">[10]</a></p>
<p>The code integrity features in recent versions of Windows can be used to limit the functionality of PowerShell, preventing or hampering malicious PowerShell in the event of a successful intrusion.</p>
<p>A combination of script code signing, application allow listing, and constrained language mode will prevent or limit the effect of malicious PowerShell in the event of a successful intrusion. These controls will also impact legitimate PowerShell scripts and it is strongly advised that they be thoroughly tested before deployment.</p>
<p>When organizations profile their PowerShell usage, they often find it is only used legitimately by a small number of technical staff. Establishing the extent of this legitimate activity will make it easier to monitor and investigate suspicious or unexpected PowerShell usage elsewhere on the network.</p>
<h4><a id=" HUC Packet Transmitter">C2 Obfuscation and Exfiltration: HUC Packet Transmitter</a> </h4>
<p>Attackers will often want to disguise their location when compromising a target. To do this, they may use generic privacy tools (e.g., Tor) or more specific tools to obfuscate their location.</p>
<p>HUC Packet Transmitter (HTran) is a proxy tool used to intercept and redirect Transmission Control Protocol (TCP) connections from the local host to a remote host. This makes it possible to obfuscate an attacker’s communications with victim networks. The tool has been freely available on the internet since at least 2009.</p>
<p>HTran facilitates TCP connections between the victim and a hop point controlled by a threat actor. Malicious threat actors can use this technique to redirect their packets through multiple compromised hosts running HTran to gain greater access to hosts in a network.</p>
<h5>In Use</h5>
<p>The use of HTran has been regularly observed in compromises of both government and industry targets.</p>
<p>A broad range of threat actors have been observed using HTran and other connection proxy tools to</p>
<ul><li>Evade intrusion and detection systems on a network,</li>
<li>Blend in with common traffic or leverage domain trust relationships to bypass security controls,</li>
<li>Obfuscate or hide C2 infrastructure or communications, and</li>
<li>Create peer-to-peer or meshed C2 infrastructure to evade detection and provide resilient connections to infrastructure.</li>
</ul><h5>Capabilities</h5>
<p>HTran can run in several modes, each of which forwards traffic across a network by bridging two TCP sockets. They differ in terms of where the TCP sockets are initiated from, either locally or remotely. The three modes are</p>
<ul><li><strong>Server (listen)</strong> – Both TCP sockets initiated remotely;</li>
<li><strong>Client (slave) </strong>– Both TCP sockets initiated locally; and</li>
<li><strong>Proxy (tran)</strong> – One TCP socket initiated remotely, the other initiated locally, upon receipt of traffic from the first connection.</li>
</ul><p>HTran can inject itself into running processes and install a rootkit to hide network connections from the host operating system. Using these features also creates Windows registry entries to ensure that HTran maintains persistent access to the victim network.</p>
<h5>Examples</h5>
<p>Recent investigations by our cybersecurity authorities have identified the use of HTran to maintain and obfuscate remote access to targeted environments.</p>
<p>In one incident, the threat actor compromised externally-facing web servers running outdated and vulnerable web applications. This access enabled the upload of webshells, which were then used to deploy other tools, including HTran.</p>
<p>HTran was installed into the ProgramData directory and other deployed tools were used to reconfigure the server to accept Remote Desktop Protocol (RDP) communications.</p>
<p>The threat actor issued a command to start HTran as a client, initiating a connection to a server located on the internet over port 80, which forwards RDP traffic from the local interface.</p>
<p>In this case, HTTP was chosen to blend in with other traffic that was expected to be seen originating from a web server to the internet. Other well-known ports used included:</p>
<ul><li>Port 53 – Domain Name System</li>
<li>Port 443 - HTTP over TLS/Secure Sockets Layer</li>
<li>Port 3306 - MySQL</li>
<li>By using HTran in this way, the threat actor was able to use RDP for several months without being detected.</li>
</ul><h5>Detection and Protection</h5>
<p>Attackers need access to a machine to install and run HTran, so network defenders should apply security patches and use good access control to prevent attackers from installing malicious applications.</p>
<p><a href="https://www.ncsc.gov.uk/guidance/introduction-logging-security-purposes">Network monitoring</a> and firewalls can help prevent and detect unauthorized connections from tools such as HTran.</p>
<p>In some of the samples analyzed, the rootkit component of HTran only hides connection details when the proxy mode is used. When client mode is used, defenders can view details about the TCP connections being made.</p>
<p>HTran also includes a debugging condition that is useful for network defenders. In the event that a destination becomes unavailable, HTran generates an error message using the following format:</p>
<div><code>sprint(buffer, “[SERVER]connection to %s:%d error\r\n”, host, port2);</code></div>
<p>This error message is relayed to the connecting client in the clear. Network defenders can monitor for this error message to potentially detect HTran instances active in their environments.</p>
<p> </p>
<div>
<h3>Mitigations</h3>
</div>
<p>There are several measures that will improve the overall cybersecurity of your organization and help protect it against the types of tools highlighted in this report. Network defenders are advised to seek further information using the links below.</p>
<ul><li>Protect your organization from malware.<br />
	See NCCIC Guidance: <a href="/ncas/tips/ST13-003">https://www.us-cert.gov/ncas/tips/ST13-003</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/protecting-your-organisation-malware">https://www.ncsc.gov.uk/guidance/protecting-your-organisation-malware</a>.</li>
<li>Board toolkit: five question for your board’s agenda.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/board-toolkit-five-questions-your-boards-agenda">https://www.ncsc.gov.uk/guidance/board-toolkit-five-questions-your-boards-agenda</a>.</li>
<li>Use a strong password policy and multifactor authentication (also known as two-factor authentication or two-step authentication) to reduce the impact of password compromises.<br />
	See NCCIC Guidance: <a href="/ncas/tips/ST05-012">https://www.us-cert.gov/ncas/tips/ST05-012</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/multi-factor-authentication-online-services">https://www.ncsc.gov.uk/guidance/multi-factor-authentication-online-services</a> and <a href="https://www.ncsc.gov.uk/guidance/setting-two-factor-authentication-2fa">https://www.ncsc.gov.uk/guidance/setting-two-factor-authentication-2fa</a>.</li>
<li>Protect your devices and networks by keeping them up to date. Use the latest supported versions, apply security patches promptly, use antivirus and scan regularly to guard against known malware threats.<br />
	See NCCIC Guidance: <a href="/ncas/tips/ST04-006">https://www.us-cert.gov/ncas/tips/ST04-006</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/mitigating-malware">https://www.ncsc.gov.uk/guidance/mitigating-malware</a>.</li>
<li>Prevent and detect lateral movement in your organization’s networks.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/preventing-lateral-movement">https://www.ncsc.gov.uk/guidance/preventing-lateral-movement</a>.</li>
<li>Implement architectural controls for network segregation.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/10-steps-network-security">https://www.ncsc.gov.uk/guidance/10-steps-network-security</a>.</li>
<li>Protect the management interfaces of your critical operational systems. In particular, use browse-down architecture to prevent attackers easily gaining privileged access to your most vital assets.<br />
	See UK NCSC blog post: <a href="https://www.ncsc.gov.uk/blog-post/protect-your-management-interfaces">https://www.ncsc.gov.uk/blog-post/protect-your-management-interfaces</a>.</li>
<li>Set up a security monitoring capability so you are collecting the data that will be needed to analyze network intrusions.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/introduction-logging-security-purposes">https://www.ncsc.gov.uk/guidance/introduction-logging-security-purposes</a>.</li>
<li>Review and refresh your incident management processes.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/10-steps-incident-management">https://www.ncsc.gov.uk/guidance/10-steps-incident-management</a>.  </li>
<li>Update your systems and software. Ensure your operating system and productivity applications are up to date. Users with Microsoft Office 365 licensing can use “click to run” to keep their office applications seamlessly updated.</li>
<li>Use modern systems and software. These have better security built-in. If you cannot move off out-of-date platforms and applications straight away, there are short-term steps you can take to improve your position.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/obsolete-platforms-security-guidance">https://www.ncsc.gov.uk/guidance/obsolete-platforms-security-guidance</a>. </li>
<li>Manage bulk personal datasets properly.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/protecting-bulk-personal-data-introduction">https://www.ncsc.gov.uk/guidance/protecting-bulk-personal-data-introduction</a>. </li>
<li>Restrict intruders' ability to move freely around your systems and networks. Pay particular attention to potentially vulnerable entry points (e.g., third-party systems with onward access to your core network). During an incident, disable remote access from third-party systems until you are sure they are clean.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/preventing-lateral-movement">https://www.ncsc.gov.uk/guidance/preventing-lateral-movement</a> and <a href="https://www.ncsc.gov.uk/guidance/assessing-supply-chain-security">https://www.ncsc.gov.uk/guidance/assessing-supply-chain-security</a>.</li>
<li>Allow list applications. If supported by your operating environment, consider allow listing of permitted applications. This will help prevent malicious applications from running.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/eud-security-guidance-windows-10-1709#applicationwhitelistingsection">https://www.ncsc.gov.uk/guidance/eud-security-guidance-windows-10-1709#applicationwhitelistingsection</a>. </li>
<li>Manage macros carefully. Disable Microsoft Office macros, except in the specific applications where they are required.<br />
	Only enable macros for users that need them day-to-day and use a recent and fully patched version of Office and the underlying platform, ideally configured in line with the UK NCSC’s End User Device Security Collection Guidance and UK NCSC’s Macro Security for Microsoft Office Guidance: <a href="https://www.ncsc.gov.uk/guidance/end-user-device-security">https://www.ncsc.gov.uk/guidance/end-user-device-security</a> and <a href="https://www.ncsc.gov.uk/guidance/macro-security-microsoft-office">https://www.ncsc.gov.uk/guidance/macro-security-microsoft-office</a>. </li>
<li>Use antivirus. Keep any antivirus software up to date, and consider use of a cloud-backed antivirus product that can benefit from the economies of scale this brings. Ensure that antivirus programs are also capable of scanning Microsoft Office macros.<br />
	See NCCIC Guidance: <a href="/ncas/tips/ST04-005">https://www.us-cert.gov/ncas/tips/ST04-005</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/macro-security-microsoft-office">https://www.ncsc.gov.uk/guidance/macro-security-microsoft-office</a>.</li>
<li>Layer organization-wide phishing defenses. Detect and quarantine as many malicious email attachments and spam as possible, before they reach your end users. Multiple layers of defense will greatly cut the chances of a compromise.</li>
<li>Treat people as your first line of defense. Tell personnel how to report suspected phishing emails, and ensure they feel confident to do so. Investigate their reports promptly and thoroughly. Never punish users for clicking phishing links or opening attachments.<br />
	NCCIC encourages users and administrators to report phishing to <a href="mailto:phishing-report@us-cert.gov">phishing-report@us-cert.gov</a>.<br />
	See NCCIC Guidance: <a href="/ncas/tips/ST04-014">https://www.us-cert.gov/ncas/tips/ST04-014</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/phishing">https://www.ncsc.gov.uk/phishing</a>. </li>
<li>Deploy a host-based intrusion detection system. A variety of products are available, free and paid-for, to suit different needs and budgets.</li>
<li>Defend your systems and networks against denial-of-service attacks.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/denial-service-dos-guidance-collection">https://www.ncsc.gov.uk/guidance/denial-service-dos-guidance-collection</a>. </li>
<li>Defend your organization from ransomware. Keep safe backups of important files, protect from malware, and do not pay the ransom– it may not get your data back.<br />
	See NCCIC Guidance: <a href="/Ransomware">https://www.us-cert.gov/Ransomware</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/mitigating-malware">https://www.ncsc.gov.uk/guidance/mitigating-malware</a> and <a href="https://www.ncsc.gov.uk/guidance/backing-your-data">https://www.ncsc.gov.uk/guidance/backing-your-data</a>.</li>
<li>Make sure you are handling personal data appropriately and securely.<br />
	See NCCIC Guidance: <a href="/ncas/tips/ST04-013">https://www.us-cert.gov/ncas/tips/ST04-013</a>.<br />
	See UK NCSC Guidance: <a href="https://www.ncsc.gov.uk/guidance/gdpr-security-outcomes">https://www.ncsc.gov.uk/guidance/gdpr-security-outcomes</a>.  </li>
</ul><p>Further information: invest in preventing malware-based attacks across various scenarios. See UK NCSC Guidance: https://www.ncsc.gov.uk/guidance/mitigating-malware.</p>
<h4>Additional Resources from International Partners</h4>
<ul><li>Australian Cyber Security Centre (ACSC) Strategies - <a href="https://acsc.gov.au/infosec/mitigationstrategies.htm">https://acsc.gov.au/infosec/mitigationstrategies.htm</a></li>
<li>ACSC Essential Eight - <a href="https://acsc.gov.au/publications/protect/essential-eight-explained.htm">https://acsc.gov.au/publications/protect/essential-eight-explained.htm</a></li>
<li>Canadian Centre for Cyber Security (CCCS) Top 10 Security Actions - <a href="https://cyber.gc.ca/en/top-10-it-security-actions">https://cyber.gc.ca/en/top-10-it-security-actions</a></li>
<li>CCCS Cyber Hygiene - <a href="https://www.cse-cst.gc.ca/en/cyberhygiene-pratiques-cybersecurite">https://www.cse-cst.gc.ca/en/cyberhygiene-pratiques-cybersecurite</a></li>
<li>CERT New Zealand's Critical Controls 2018 - <a href="https://www.cert.govt.nz/it-specialists/critical-controls/">https://www.cert.govt.nz/it-specialists/critical-controls/</a></li>
<li>CERT New Zealand’s Top 11 Cyber Security Tips for Your Business - <a href="https://www.cert.govt.nz/businesses-and-individuals/guides/cyber-security-your-business/top-11-cyber-security-tips-for-your-business/">https://www.cert.govt.nz/businesses-and-individuals/guides/cyber-security-your-business/top-11-cyber-security-tips-for-your-business/</a></li>
<li>New Zealand National Cyber Security Centre (NZ NCSC) Resources - <a href="https://www.ncsc.govt.nz/resources/">https://www.ncsc.govt.nz/resources/</a></li>
<li>New Zealand Information Security Manual - <a href="https://www.gcsb.govt.nz/the-nz-information-security-manual/">https://www.gcsb.govt.nz/the-nz-information-security-manual/</a></li>
<li>UK NCSC 10 Steps to Cyber Security - <a href="https://www.ncsc.gov.uk/guidance/10-steps-cyber-security">https://www.ncsc.gov.uk/guidance/10-steps-cyber-security</a></li>
<li>UK NCSC Board Toolkit: five questions for your board's agenda - <a href="https://www.ncsc.gov.uk/guidance/board-toolkit-five-questions-your-boards-agenda">https://www.ncsc.gov.uk/guidance/board-toolkit-five-questions-your-boards-agenda</a></li>
<li>UK NCSC Cyber Security: Small Business Guide - <a href="https://www.ncsc.gov.uk/smallbusiness">https://www.ncsc.gov.uk/smallbusiness</a></li>
</ul><div>
<h3>Contact Information</h3>
</div>
<p>NCCIC encourages recipients of this report to contribute any additional information that they may have related to this threat. For any questions related to this report, please contact NCCIC at</p>
<ul><li>1-888-282-0870 (From outside the United States: +1-703-235-8832)</li>
<li><a href="mailto:NCCICCustomerService@us-cert.gov">NCCICCustomerService@us-cert.gov</a> (UNCLASS)</li>
<li><a href="mailto:us-cert@dhs.sgov.gov">us-cert@dhs.sgov.gov</a> (SIPRNET)</li>
<li><a href="mailto:us-cert@dhs.ic.gov">us-cert@dhs.ic.gov</a> (JWICS)</li>
</ul><p>NCCIC encourages you to report any suspicious activity, including cybersecurity incidents, possible malicious code, software vulnerabilities, and phishing-related scams. Reporting forms can be found on the NCCIC/US-CERT homepage at <a href="/">http://www.us-cert.gov/</a>.</p>
<h4>Feedback</h4>
<p>NCCIC strives to make this report a valuable tool for our partners and welcomes feedback on how this publication could be improved. You can help by answering a few short questions about this report at the following URL: <a href="/forms/feedback">https://www.us-cert.gov/forms/feedback</a>.</p>
<div>
<h3>References</h3>
</div>
<div class="field--item"><a href="https://www.acsc.gov.au">[1] Australian Cyber Security Centre (ACSC)</a></div>
<div class="field--item"><a href="https://cyber.gc.ca/en">[2] Canadian Centre for Cyber Security (CCCS)</a></div>
<div class="field--item"><a href="https://www.ncsc.govt.nz">[3] New Zealand National Cyber Security Centre (NZ NCSC)</a></div>
<div class="field--item"><a href="https://www.ncsc.gov.uk">[4] UK National Cyber Security Centre (UK NCSC)</a></div>
<div class="field--item"><a href="https://www.us-cert.gov">[5] US National Cybersecurity and Communications Integration Center </a></div>
<div class="field--item"><a href="http://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project">[6] OWASP Top 10 Project </a></div>
<div class="field--item"><a href="https://www.fireeye.com/blog/threat-research/2013/08/breaking-down-the-china-chopper-web-shell-part-ii.html">[7] FireEye Report on China Chopper</a></div>
<div class="field--item"><a href="https://support.microsoft.com/en-us/help/2871997/microsoft-security-advisory-update-to-improve-credentials-protection-a">[8] Microsoft Security Advisory</a></div>
<div class="field--item"><a href="https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory">[9] Microsoft - Best Practices for Securing Active Directory</a></div>
<div class="field--item"><a href="https://www.digitalshadows.com/blog-and-research/powershell-security-best-practices">[10] Digital Shadows - PowerShell Security Best Practices</a></div>
<div>
<h3>Revisions</h3>
</div>
<p>October, 11 2018: Initial version</p>

      </div>

  
      </div>
  </div>
      <div class="l-constrain l-page-section--rich-text">
        <div class="l-page-section__content">
          




<div  class="c-field c-field--name-body c-field--type-text-with-summary c-field--label-hidden">
  <div class="c-field__content"><p>This product is provided subject to this <a href="/notification" rel="nofollow noopener" target="_blank" title="Follow link">Notification</a> and this <a href="/privacy-policy" rel="nofollow noopener" target="_blank" title="Follow link">Privacy &amp; Use</a> policy.</p></div></div>

        </div>
      </div>
            </div>
        <div class="l-full__footer">
                              
<div class="l-constrain">
  <div class="l-page-section--rich-text">
    <div class="l-page-section__content">
      <div  class="c-product-survey l-page-section--tags l-page-section--rich-text">
        <div class="c-product-survey__top-bar"></div>
        <div class="c-product-survey__content-area">
          <div class="c-product-survey__icon"></div>
          <div class="c-product-survey__text-area">
            <h2>Please share your thoughts</h2>
            <p>We recently updated our anonymous <a href="https://www.surveymonkey.com/r/CISA-cyber-survey?product=https://www.cisa.gov/news-events/cybersecurity-advisories/aa18-284a">product survey</a>; we’d welcome your feedback.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
          

  

<div  class="c-view c-view--detail-page-related-content c-view--display-block_2 view js-view-dom-id-b7f65e09d0b9f268a335f5e91b795b2e9a0790944745245fdc7a80fdf9368b76 c-collection c-collection--blue c-collection--two-column">
  <div class="l-constrain">
    <div class="c-collection__row">
              <div class="c-collection__content">
                      <h2 class="c-collection__title"><span class="c-collection__title-wrap">Related Advisories</span></h2>
                                      </div>
                  <div class="c-collection__cards">
        



      





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2023-11-21T12:00:00Z">Nov 21, 2023</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA23-325A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa23-325a" target="_self">          
<span>#StopRansomware: LockBit 3.0 Ransomware Affiliates Exploit CVE 2023-4966 Citrix Bleed Vulnerability</span>

        </a>      </h3>
                            </div>
  </div>
</article>


        





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2023-11-16T12:00:00Z">Nov 16, 2023</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA23-320A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa23-320a" target="_self">          
<span>Scattered Spider</span>

        </a>      </h3>
                            </div>
  </div>
</article>


        





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2023-11-15T12:00:00Z">Nov 15, 2023</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA23-319A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa23-319a" target="_self">          
<span>#StopRansomware: Rhysida Ransomware</span>

        </a>      </h3>
                            </div>
  </div>
</article>


        





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2023-10-16T12:00:00Z">Oct 16, 2023</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA23-289A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa23-289a" target="_self">          
<span>Threat Actors Exploit Atlassian Confluence CVE-2023-22515 for Initial Access to Networks</span>

        </a>      </h3>
                            </div>
  </div>
</article>


  
      </div>
    </div>
          </div>
</div>


          </div>
  </div>
  
  
  
  

      </div>

  
  </main>

  

<footer  class="usa-footer usa-footer--slim" role="contentinfo">
    <div class="usa-footer__return-to-top">
    <div class="l-constrain">
      <a href="#">Return to top</a>
    </div>
  </div>
    <div class="usa-footer__upper">
    <div class="l-constrain">
      







  
  
    

  
            

                                <ul  class="c-menu c-menu--footer-main">
        
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/topics" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7329">Topics</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/spotlight" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7330">Spotlight</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/resources-tools" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7331">Resources &amp; Tools</a>
                        </li>
    
                                            
                                                    
      
      
      <li  class="c-menu__item is-active-trail">
                              <a href="/news-events" class="c-menu__link js-top-level is-active-trail" aria-current="false" data-drupal-link-system-path="node/7332">News &amp; Events</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/careers" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7323">Careers</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/about" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/6944">About</a>
                        </li>
        </ul>
  

  
  
  
  

    </div>
  </div>
    <div class="usa-footer__main">
    <div class="l-constrain">
      <div class="usa-footer__main-row">
        <div class="usa-footer__brand">
          
<a  class="c-site-name c-site-name--footer" href="/" rel="home" title="Go to the Cybersecurity & Infrastructure Security Agency homepage">
  <span class="c-site-name__text">Cybersecurity &amp; Infrastructure Security Agency</span>
</a>        </div>
        <div class="usa-footer__contact">
                      

                                <ul  class="c-menu c-menu--social">
        
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.facebook.com/CISA" class="c-menu__link--facebook c-menu__link js-top-level" aria-current="false">Facebook</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://twitter.com/CISAgov" class="c-menu__link--twitter c-menu__link js-top-level" aria-current="false">Twitter</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.linkedin.com/company/cybersecurity-and-infrastructure-security-agency" class="c-menu__link--linkedin c-menu__link js-top-level" aria-current="false">LinkedIn</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.youtube.com/@cisagov" class="c-menu__link--youtube c-menu__link js-top-level" aria-current="false">YouTube</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.instagram.com/cisagov" class="c-menu__link--instagram c-menu__link js-top-level" aria-current="false">Instagram</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="/subscribe-updates-cisa" class="c-menu__link--rss c-menu__link js-top-level" aria-current="false">RSS</a>
                        </li>
        </ul>
  

                    <div class="usa-footer__contact-info">
            <span>CISA Central</span>
            <a href="tel:8882820870">888-282-0870</a>
            <a href="mailto:central@cisa.dhs.gov">Central@cisa.dhs.gov</a>
          </div>
        </div>
      </div>
    </div>
  </div>
    <div class="usa-footer__lower">
    <div class="l-constrain">
      <div class="usa-footer__lower-row">
        <div class="usa-footer__lower-left">
          
<div  class="c-dhs-logo">
  <div class="c-dhs-logo__seal">DHS Seal</div>
  <div class="c-dhs-logo__content">
    <div class="c-dhs-logo__url">CISA.gov</div>
    <div class="c-dhs-logo__text">An official website of the U.S. Department of Homeland Security</div>
  </div>
</div>                      


                                <ul  class="c-menu c-menu--footer">
        
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/about" class="c-menu__link js-top-level" title="About CISA" aria-current="false" data-drupal-link-system-path="node/6944">About CISA</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov/accessibility" class="c-menu__link js-top-level" title="Accessibility" aria-current="false">Accessibility</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov/performance-financial-reports" class="c-menu__link js-top-level" title="Budget and Performance" aria-current="false">Budget and Performance</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov" title="Department of Homeland Security" class="c-menu__link js-top-level" aria-current="false">DHS.gov</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov/foia" class="c-menu__link js-top-level" title="FOIA Requests" aria-current="false">FOIA Requests</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/cisa-no-fear-act-reporting" title="No FEAR Act Reporting" class="c-menu__link js-top-level" aria-current="false">No FEAR Act</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.oig.dhs.gov/" class="c-menu__link js-top-level" title="Office of Inspector General" aria-current="false">Office of Inspector General</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/privacy-policy" class="c-menu__link js-top-level" title="Privacy Policy" aria-current="false" data-drupal-link-system-path="node/16115">Privacy Policy</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://public.govdelivery.com/accounts/USDHSCISA/subscriber/new?topic_id=USDHSCISA_138" title="Subscribe to Email Updates" class="c-menu__link js-top-level" aria-current="false">Subscribe</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.whitehouse.gov/" class="c-menu__link js-top-level" title="The White House" aria-current="false">The White House</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.usa.gov/" class="c-menu__link js-top-level" title="USA.gov" aria-current="false">USA.gov</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/forms/feedback" title="Website Feedback" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="forms/feedback">Website Feedback</a>
                        </li>
        </ul>
  

                  </div>
        <div class="usa-footer__lower-right">
          <iframe
            src="https://www.dhs.gov/ntas/"
            name="National Terrorism Advisory System"
            title="National Terrorism Advisory System"
            width="170"
            height="180"
            scrolling="no"
            frameborder="0"
            seamless border="0"
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</footer>


</div>

  </div>

    
        <script type="application/json" data-drupal-selector="drupal-settings-json">{"path":{"baseUrl":"\/","scriptPath":null,"pathPrefix":"","currentPath":"node\/8353","currentPathIsAdmin":false,"isFront":false,"currentLanguage":"en"},"pluralDelimiter":"\u0003","suppressDeprecationErrors":true,"google_analytics":{"account":"G-9MDR73GM0K","trackOutbound":true,"trackMailto":true,"trackTel":true,"trackDownload":true,"trackDownloadExtensions":"7z|aac|arc|arj|asf|asx|avi|bin|csv|doc(x|m)?|dot(x|m)?|exe|flv|gif|gz|gzip|hqx|jar|jpe?g|js|mp(2|3|4|e?g)|mov(ie)?|msi|msp|pdf|phps|png|ppt(x|m)?|pot(x|m)?|pps(x|m)?|ppam|sld(x|m)?|thmx|qtm?|ra(m|r)?|sea|sit|tar|tgz|torrent|txt|wav|wma|wmv|wpd|xls(x|m|b)?|xlt(x|m)|xlam|xml|z|zip"},"data":{"extlink":{"extTarget":false,"extTargetNoOverride":false,"extNofollow":false,"extNoreferrer":false,"extFollowNoOverride":false,"extClass":"ext","extLabel":"(link is external)","extImgClass":false,"extSubdomains":true,"extExclude":"(.\\.gov$)|(.\\.mil$)|(.\\.mil\/)|(.\\.gov\/)","extInclude":"","extCssExclude":".c-menu--social,.c-menu--footer,.c-social-links,.c-text-cta--button","extCssExplicit":"","extAlert":true,"extAlertText":"You are now leaving an official website of the United State Government (USG), the Department of Homeland Security (DHS) and the Cybersecurity and Infrastructure Security Agency (CISA). Links to non-USG, non-DHS and non-CISA sites are provided for the visitor\u0027s convenience and do not represent an endorsement by USG, DHS or CISA of any commercial or private issues, products or services. Note that the privacy policy of the linked site may differ from that of USG, DHS and CISA.","mailtoClass":"mailto","mailtoLabel":"(link sends email)","extUseFontAwesome":false,"extIconPlacement":"append","extFaLinkClasses":"fa fa-external-link","extFaMailtoClasses":"fa fa-envelope-o","whitelistedDomains":[]}},"ckeditorExpandableTextbox":{"accordionStyle":{"collapseAll":true,"keepRowsOpen":false}},"ckeditorAccordion":{"accordionStyle":{"collapseAll":1,"keepRowsOpen":0,"animateAccordionOpenAndClose":1,"openTabsWithHash":1}},"user":{"uid":0,"permissionsHash":"2e28e3d4cecae698758a87360e5c783a3a6bbf12a454265e787234af3fdfaba5"}}</script>
<script src="/core/assets/vendor/jquery/jquery.min.js?v=3.7.0"></script>
<script src="/core/assets/vendor/once/once.min.js?v=1.0.1"></script>
<script src="/core/misc/drupalSettingsLoader.js?v=10.1.5"></script>
<script src="/core/misc/drupal.js?v=10.1.5"></script>
<script src="/core/misc/drupal.init.js?v=10.1.5"></script>
<script src="/modules/contrib/google_analytics/js/google_analytics.js?v=10.1.5"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/common.js?s4w5q2"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/uswds-init.es6.js?s4w5q2"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/uswds.es6.js?s4w5q2"></script>
<script src="https://dap.digitalgov.gov/Universal-Federated-Analytics-Min.js?" id="_fed_an_ua_tag"></script>
<script src="/modules/contrib/extlink/extlink.js?v=10.1.5"></script>
<script src="/profiles/cisad8_gov/modules/custom/cisa_core/js/ckeditor-expandabletextbox.js?v=1.1.x"></script>
<script src="/modules/contrib/ckeditor_accordion/js/accordion.frontend.js?s4w5q2"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/teaser.es6.js?s4w5q2"></script>
<script src="/modules/contrib/responsive_tables_filter/js/tablesaw.min.js?v=1.x"></script>
<script src="/modules/contrib/responsive_tables_filter/js/tablesaw-init.js?v=1.x"></script>
<script src="/modules/contrib/responsive_tables_filter/js/Drupal/ajaxComplete.js?v=1.x"></script>
<script src="/modules/contrib/responsive_tables_filter/js/customizations.js?v=1.x"></script>

  </body>
</html>

"""
html = """
<!DOCTYPE html>
<html lang="en" dir="ltr" prefix="og: https://ogp.me/ns#" class="no-js">
  <head>
    <meta charset="utf-8" />
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MDR73GM0K"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments)};gtag("js", new Date());gtag("set", "developer_id.dMDhkMT", true);gtag("config", "G-9MDR73GM0K", {"groups":"default","page_placeholder":"PLACEHOLDER_page_location"});</script>
<meta name="description" content="View Cybersecurity Advisories OnlyView Advisory Definitions" />
<link rel="canonical" href="https://www.cisa.gov/news-events/cybersecurity-advisories" />
<meta property="og:site_name" content="Cybersecurity and Infrastructure Security Agency CISA" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://www.cisa.gov/news-events/cybersecurity-advisories" />
<meta property="og:title" content="Cybersecurity Alerts &amp; Advisories | CISA" />
<meta property="og:description" content="View Cybersecurity Advisories OnlyView Advisory Definitions" />
<meta name="Generator" content="Drupal 10 (https://www.drupal.org)" />
<meta name="MobileOptimized" content="width" />
<meta name="HandheldFriendly" content="true" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" href="/profiles/cisad8_gov/themes/custom/gesso/favicon.png" type="image/png" />

    <title>Cybersecurity Alerts &amp; Advisories | CISA</title>
    <link rel="stylesheet" media="all" href="/core/modules/system/css/components/ajax-progress.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/align.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/autocomplete-loading.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/fieldgroup.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/container-inline.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/clearfix.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/details.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/hidden.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/item-list.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/js.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/nowrap.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/position-container.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/progress.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/reset-appearance.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/resize.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/sticky-header.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/system-status-counter.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/system-status-report-counters.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/system-status-report-general-info.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/tabledrag.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/tablesort.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/system/css/components/tree-child.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/facets/modules/facets_searchbox_widget/css/searchbox.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/views/css/views.module.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/profiles/cisad8_gov/modules/custom/toolbar_tasks/css/toolbar.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/extlink/extlink.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/profiles/cisad8_gov/modules/custom/cisa_core/css/ckeditor-expandabletextbox.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/ckeditor_accordion/css/accordion.frontend.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/layout_builder/layouts/twocol_section/twocol_section.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/core/modules/layout_discovery/layouts/onecol/onecol.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/better_social_sharing_buttons/css/better_social_sharing_buttons.css?s4w5q2" />
<link rel="stylesheet" media="all" href="/modules/contrib/paragraphs/css/paragraphs.unpublished.css?s4w5q2" />
<link rel="stylesheet" media="all" href="//fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;family=Public+Sans:wght@400;500;600;700&amp;display=swap" />
<link rel="stylesheet" media="all" href="/profiles/cisad8_gov/themes/custom/gesso/dist/css/styles.css?s4w5q2" />

    
  </head>
  <body  class="path-node not-front node-page node-page--node-type-flexible-page" id="top">
    
<div  class="c-skiplinks">
  <a href="#main" class="c-skiplinks__link u-visually-hidden u-focusable">Skip to main content</a>
</div>
    
      <div class="dialog-off-canvas-main-canvas" data-off-canvas-main-canvas>
    

<div  class="l-site-container">
    
      
<section  class="usa-banner" aria-label="Official government website">
  <div class="usa-accordion">  <header class="usa-banner__header">
    <div class="usa-banner__inner">
      <div class="grid-col-auto">
        <img class="usa-banner__header-flag" src="/profiles/cisad8_gov/themes/custom/gesso/dist/images/us_flag_small.png" alt="U.S. flag" />
      </div>
      <div class="grid-col-fill tablet:grid-col-auto">
        <p class="usa-banner__header-text">An official website of the United States government</p>
              <p class="usa-banner__header-action" aria-hidden="true">Here’s how you know</p></div>
        <button class="usa-accordion__button usa-banner__button" aria-expanded="false" aria-controls="gov-banner">
          <span class="usa-banner__button-text">Here’s how you know</span>
        </button>
          </div>
  </header>
      <div class="usa-banner__content usa-accordion__content" id="gov-banner">
      <div class="grid-row grid-gap-lg">
                  <div class="usa-banner__guidance tablet:grid-col-6">
            <img class="usa-banner__icon usa-media-block__img" src="/profiles/cisad8_gov/themes/custom/gesso/dist/images/icon-dot-gov.svg" alt="Dot gov">
            <div class="usa-media-block__body">
              <p>
                <strong>Official websites use .gov</strong>
                <br> A <strong>.gov</strong> website belongs to an official government organization in the United States.
              </p>
            </div>
          </div>
                  <div class="usa-banner__guidance tablet:grid-col-6">
            <img class="usa-banner__icon usa-media-block__img" src="/profiles/cisad8_gov/themes/custom/gesso/dist/images/icon-https.svg" alt="HTTPS">
            <div class="usa-media-block__body">
              <p>
                <strong>Secure .gov websites use HTTPS</strong>
                <br> A <strong>lock</strong> (<span class="icon-lock"><svg xmlns="http://www.w3.org/2000/svg" width="52" height="64" viewBox="0 0 52 64" class="usa-banner__lock-image" role="img" aria-labelledby="banner-lock-title banner-lock-description"><title id="banner-lock-title">Lock</title><desc id="banner-lock-description">A locked padlock</desc><path fill="#000000" fill-rule="evenodd" d="M26 0c10.493 0 19 8.507 19 19v9h3a4 4 0 0 1 4 4v28a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V32a4 4 0 0 1 4-4h3v-9C7 8.507 15.507 0 26 0zm0 8c-5.979 0-10.843 4.77-10.996 10.712L15 19v9h22v-9c0-6.075-4.925-11-11-11z"/></svg></span>) or <strong>https://</strong> means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.
              </p>
            </div>
          </div>
              </div>
    </div>
  </div>
  </section>

  
  


<div class="usa-overlay"></div>
<header  class="usa-header usa-header--extended" role="banner">
        
<div  class="usa-navbar">
  <div class="l-constrain">
    <div class="usa-navbar__row">
      <div class="usa-navbar__brand">
        
<a  class="c-site-name" href="/" rel="home" title="Go to the Cybersecurity & Infrastructure Security Agency homepage">
  <span class="c-site-name__text">Cybersecurity &amp; Infrastructure Security Agency</span>
</a>        <div class="usa-navbar__tagline">America's Cyber Defense Agency</div>
      </div>
      <div class="usa-navbar__search">
        <div class="usa-navbar__search-header">
          <p>Search</p>
        </div>
        
<div  class="usa-search">
  <script async src=https://cse.google.com/cse.js?cx=ffc4c79e29d5b3a8c></script>
  <div class="gcse-searchbox-only" data-resultsurl="/search">&nbsp;</div>
</div>
      </div>
      <button class="mobile-menu-button usa-menu-btn">Menu</button>
    </div>
  </div>
</div>
    

<nav  class="usa-nav" role="navigation" aria-label="Primary navigation">
  <div class="usa-nav__inner l-constrain">
    <div class="usa-nav__row">
      <button class="usa-nav__close">Close</button>
      
<div  class="usa-search">
  <script async src=https://cse.google.com/cse.js?cx=ffc4c79e29d5b3a8c></script>
  <div class="gcse-searchbox-only" data-resultsurl="/search">&nbsp;</div>
</div>
                
  
          <ul class="usa-nav__primary usa-accordion">
    
    
              <li class="usa-nav__primary-item topics">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-1">
          <span>Topics</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-1" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/topics">Topics</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/cybersecurity-best-practices">
          <span>Cybersecurity Best Practices</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/cyber-threats-and-advisories">
          <span>Cyber Threats and Advisories</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/critical-infrastructure-security-and-resilience">
          <span>Critical Infrastructure Security and Resilience</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/election-security">
          <span>Election Security</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/emergency-communications">
          <span>Emergency Communications</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/industrial-control-systems">
          <span>Industrial Control Systems</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/information-communications-technology-supply-chain-security">
          <span>Information and Communications Technology Supply Chain Security</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/partnerships-and-collaboration">
          <span>Partnerships and Collaboration</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/physical-security">
          <span>Physical Security</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/topics/risk-management">
          <span>Risk Management</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          

<div  class="c-menu-feature-links">
      <div class="c-menu-feature-links__title">
      <a href="/audiences">        How can we help?
      </a>    </div>
        <div class="c-menu-feature-links__content"><a href="/topics/government">Government</a><a href="/topics/educational-institutions">Educational Institutions</a><a href="/topics/industry">Industry</a><a href="/topics/state-local-tribal-and-territorial">State, Local, Tribal, and Territorial</a><a href="/topics/individuals-and-families">Individuals and Families</a><a href="/topics/small-and-medium-businesses">Small and Medium Businesses</a><a href="/audiences/find-help-locally">Find Help Locally</a><a href="/audiences/faith-based-community">Faith-Based Community</a><a href="/audiences/executives">Executives</a></div>
  </div>

              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item spotlight">
      
      
                      <a href="/spotlight" class="usa-nav__link" >
          <span>Spotlight</span>
        </a>
              
              </li>
          
              <li class="usa-nav__primary-item resources--tools">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-3">
          <span>Resources &amp; Tools</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-3" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/resources-tools">Resources &amp; Tools</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/all-resources-tools">
          <span>All Resources &amp; Tools</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/services">
          <span>Services</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/programs">
          <span>Programs</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/resources">
          <span>Resources</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/training">
          <span>Training</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/resources-tools/groups">
          <span>Groups</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item news--events">
      
              <button class="usa-accordion__button usa-nav__link usa-current" aria-expanded="false" aria-controls="basic-mega-nav-section-4">
          <span>News &amp; Events</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-4" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/news-events">News &amp; Events</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/news">
          <span>News</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/events">
          <span>Events</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/cybersecurity-advisories">
          <span>Cybersecurity Alerts &amp; Advisories</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/directives">
          <span>Directives</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/request-speaker">
          <span>Request a CISA Speaker</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/news-events/congressional-testimony">
          <span>Congressional Testimony</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item careers">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-5">
          <span>Careers</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-5" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/careers">Careers</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/benefits-perks">
          <span>Benefits &amp; Perks</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/hirevue-applicant-reasonable-accommodations-process">
          <span>HireVue Applicant Reasonable Accommodations Process</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/general-recruitment-and-hiring-faqs">
          <span>Hiring</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/resume-application-tips">
          <span>Resume &amp; Application Tips</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/students-recent-graduates-employment-opportunities">
          <span>Students &amp; Recent Graduates</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/veteran-and-military-spouse-employment-opportunities">
          <span>Veteran and Military Spouses</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/careers/work-cisa">
          <span>Work @ CISA</span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
              <li class="usa-nav__primary-item about">
      
              <button class="usa-accordion__button usa-nav__link " aria-expanded="false" aria-controls="basic-mega-nav-section-6">
          <span>About</span>
        </button>
      
                
  
          <div id="basic-mega-nav-section-6" class="usa-nav__submenu usa-megamenu" hidden="">

              <div class="usa-megamenu__parent-link">
          <a href="/about">About</a>
        </div>
              <div class="usa-megamenu__menu-items">
    
    
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/culture">
          <span>Culture</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/divisions-offices">
          <span>Divisions &amp; Offices</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/regions">
          <span>Regions</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/leadership">
          <span>Leadership</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/doing-business-cisa">
          <span>Doing Business with CISA</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/site-links">
          <span>Site Links</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/reporting-employee-and-contractor-misconduct">
          <span>Reporting Employee and Contractor Misconduct</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/cisa-github">
          <span>CISA GitHub</span>
        </a>
                  </div>
              
              </div>
          
              <div class="usa-col">

              
      
                        <div class="usa-nav__submenu-item">
                <a href="/about/contact-us">
          <span>Contact Us </span>
        </a>
                  </div>
              
              </div>
          
            </div>
                          
              </div>
    
  
      
              </li>
          
    
      </ul>
    
  


                    <a href="/report" class="c-button c-button--report">Report a Cyber Issue</a>
          </div>
  </div>
</nav>
    </header>


  <div class="gesso-mobile-tagline-container">
    <div class="usa-navbar__tagline">America's Cyber Defense Agency</div>
  </div>

  
  
<div  class="l-breadcrumb">
  <div class="l-constrain">
    <div class="l-breadcrumb__row">
      







  
  
    

  
              


<nav  aria-labelledby="breadcrumb-label" class="c-breadcrumb" role="navigation">
  <div class="l-constrain">
    <div
       id="breadcrumb-label" class="c-breadcrumb__title  u-visually-hidden">Breadcrumb</div>
    <ol class="c-breadcrumb__list">
              <li class="c-breadcrumb__item">
                      <a class="c-breadcrumb__link" href="/">Home</a>
                  </li>
              <li class="c-breadcrumb__item">
                      <a class="c-breadcrumb__link" href="/news-events">News &amp; Events</a>
                  </li>
          </ol>
  </div>
</nav>

  
  
  
  






  <div  id="block-bettersocialsharingbuttons" class="c-block c-block--social-share c-block--provider-better-social-sharing-buttons c-block--id-social-sharing-buttons-block">

  
  
    

      <div  class="c-block__content">
  
      <div class="c-block__row">
      <span>Share:</span>
      

<div style="display: none"><link rel="preload" href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg" as="image" type="image/svg+xml" crossorigin="anonymous" /></div>

<div class="social-sharing-buttons">
                <a href="https://www.facebook.com/sharer/sharer.php?u=https://www.cisa.gov/news-events/cybersecurity-advisories&amp;title=Cybersecurity%20Alerts%20%26%20Advisories" target="_blank" title="Share to Facebook" aria-label="Share to Facebook" class="social-sharing-buttons__button share-facebook" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#facebook" />
            </svg>
        </a>
    
                <a href="https://twitter.com/intent/tweet?text=Cybersecurity%20Alerts%20%26%20Advisories+https://www.cisa.gov/news-events/cybersecurity-advisories" target="_blank" title="Share to Twitter" aria-label="Share to Twitter" class="social-sharing-buttons__button share-twitter" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#twitter" />
            </svg>
        </a>
    
        
        
        
                <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://www.cisa.gov/news-events/cybersecurity-advisories" target="_blank" title="Share to Linkedin" aria-label="Share to Linkedin" class="social-sharing-buttons__button share-linkedin" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#linkedin" />
            </svg>
        </a>
    
        
        
        
        
        
                <a href="mailto:?subject=Cybersecurity%20Alerts%20%26%20Advisories&amp;body=https://www.cisa.gov/news-events/cybersecurity-advisories" title="Share to Email" aria-label="Share to Email" class="social-sharing-buttons__button share-email" target="_blank" rel="noopener">
            <svg width="18px" height="18px" style="border-radius:3px;">
                <use href="/modules/contrib/better_social_sharing_buttons/assets/dist/sprites/social-icons--no-color.svg#email" />
            </svg>
        </a>
    
        
    </div>

    </div>
  
      </div>
  
  
  </div>

    </div>
  </div>
</div>

  
  

  <main id="main" class="c-main" role="main" tabindex="-1">
    
      
    


<div  class="l-content">
          







  
  
    

  
            




  
  
  

  
  
  
  


<div  class="l-sidebar has-aside-left  has-no-header l-sidebar--listing">

  
  <div class="l-sidebar__row">
          <aside class="l-sidebar__left">
              





  <div  class="views-exposed-form c-block c-block--provider-views c-block--id-views-exposed-filter-blockindex-advisory-listing-block-1 c-block c-block--exposed-filter" data-drupal-selector="views-exposed-form-index-advisory-listing-block-1">

  
  
    

      <div  class="c-block__content">
  
      <h3>Filters</h3>
    <p>What are you looking for?</p>
    <form action="/news-events/cybersecurity-advisories" method="get" id="views-exposed-form-index-advisory-listing-block-1" accept-charset="UTF-8">
  



  
  
<div  class="c-form-item c-form-item--text       c-form-item--id-search-api-fulltext js-form-item js-form-type-textfield js-form-item-search-api-fulltext">
            




<label  for="edit-search-api-fulltext" class="c-form-item__label">Text Search

  <span class="usa-hint">
        (optional)
      </span></label>

      
  
    
    
    





  












<input  data-drupal-selector="edit-search-api-fulltext" type="text" id="edit-search-api-fulltext" name="search_api_fulltext" value="" size="30" maxlength="128" class="c-form-item__text">



    
    
  
  
  </div>




  
  
<div  class="c-form-item c-form-item--select       c-form-item--id-sort-by js-form-item js-form-type-select js-form-item-sort-by">
            




<label  for="edit-sort-by" class="c-form-item__label">Sort by

  <span class="usa-hint">
        (optional)
      </span></label>

      
  
    
    
    







<select  data-drupal-selector="edit-sort-by" id="edit-sort-by" name="sort_by" class="c-form-item__select c-form-item--select"><option value="field_release_date" selected="selected">Release Date</option><option value="field_last_updated">Last Revised</option><option value="label">Title</option><option value="relevance">Relevance</option><option value="field_vendor_name">Vendor</option></select>

    
    
  
  
  </div>

<div data-drupal-selector="edit-actions" class="form-actions js-form-wrapper" id="edit-actions">





  












<input  data-drupal-selector="edit-submit-index-advisory-listing" type="submit" id="edit-submit-index-advisory-listing" value="Apply" class="c-button js-form-submit c-form-item__submit c-button js-form-submit">

</div>


</form>

  
      </div>
  
  
  </div>






  <div  class="facet-active block-facet--checkbox c-block c-block--facet-block c-block--provider-facets c-block--id-facet-blockadvisory-type">

  
  
    

  
      


<div  class="c-facet-block">
      <button class="c-facet-block__trigger" aria-expanded="false">
      <h3 class="c-facet-block__title">Advisory Type</h3>
    </button>
    <div class="c-facet-block__content" aria-hidden="true">
    


<div  class="facets-widget-checkbox">
      <ul data-drupal-facet-id="advisory_type" data-drupal-facet-alias="advisory_type" class="facet-active js-facets-checkbox-links item-list__checkbox"><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A93&amp;f%5B1%5D=advisory_type%3A94" rel="nofollow" data-drupal-facet-item-id="advisory-type-93" data-drupal-facet-item-value="93" data-drupal-facet-item-count="3920"><span class="facet-item__value c-facet-summary__value">Alert</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A65&amp;f%5B1%5D=advisory_type%3A94" rel="nofollow" data-drupal-facet-item-id="advisory-type-65" data-drupal-facet-item-value="65" data-drupal-facet-item-count="127"><span class="facet-item__value c-facet-summary__value">Analysis Report</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories" rel="nofollow" class="is-active" data-drupal-facet-item-id="advisory-type-94" data-drupal-facet-item-value="94" data-drupal-facet-item-count="135">  <span class="facet-item__status c-facet-summary__status js-facet-deactivate">(-)</span>
<span class="facet-item__value c-facet-summary__value">Cybersecurity Advisory</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=advisory_type%3A95" rel="nofollow" data-drupal-facet-item-id="advisory-type-95" data-drupal-facet-item-value="95" data-drupal-facet-item-count="2528"><span class="facet-item__value c-facet-summary__value">ICS Advisory</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=advisory_type%3A96" rel="nofollow" data-drupal-facet-item-id="advisory-type-96" data-drupal-facet-item-value="96" data-drupal-facet-item-count="139"><span class="facet-item__value c-facet-summary__value">ICS Medical Advisory</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=advisory_type%3A97" rel="nofollow" data-drupal-facet-item-id="advisory-type-97" data-drupal-facet-item-value="97" data-drupal-facet-item-count="141"><span class="facet-item__value c-facet-summary__value">ICS Alert</span>
</a>
                                  </li></ul>


</div>

  </div>
</div>
  
  
  
  </div>






  <div  class="facet-inactive block-facet--checkbox c-block c-block--facet-block c-block--provider-facets c-block--id-facet-blockadvisory-release-date-year">

  
  
    

  
      


<div  class="c-facet-block">
      <button class="c-facet-block__trigger" aria-expanded="false">
      <h3 class="c-facet-block__title">Release Year</h3>
    </button>
    <div class="c-facet-block__content" aria-hidden="true">
    


<div  class="facets-widget-checkbox">
      <ul data-drupal-facet-id="advisory_release_date_year" data-drupal-facet-alias="release_date_year" class="facet-inactive js-facets-checkbox-links item-list__checkbox"><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=release_date_year%3A2023" rel="nofollow" data-drupal-facet-item-id="release-date-year-2023" data-drupal-facet-item-value="2023" data-drupal-facet-item-count="30"><span class="facet-item__value c-facet-summary__value">2023</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=release_date_year%3A2022" rel="nofollow" data-drupal-facet-item-id="release-date-year-2022" data-drupal-facet-item-value="2022" data-drupal-facet-item-count="36"><span class="facet-item__value c-facet-summary__value">2022</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=release_date_year%3A2021" rel="nofollow" data-drupal-facet-item-id="release-date-year-2021" data-drupal-facet-item-value="2021" data-drupal-facet-item-count="24"><span class="facet-item__value c-facet-summary__value">2021</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=release_date_year%3A2020" rel="nofollow" data-drupal-facet-item-id="release-date-year-2020" data-drupal-facet-item-value="2020" data-drupal-facet-item-count="38"><span class="facet-item__value c-facet-summary__value">2020</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=release_date_year%3A2019" rel="nofollow" data-drupal-facet-item-id="release-date-year-2019" data-drupal-facet-item-value="2019" data-drupal-facet-item-count="5"><span class="facet-item__value c-facet-summary__value">2019</span>
</a>
                                  </li><li class="facet-item">
            <a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&amp;f%5B1%5D=release_date_year%3A2018" rel="nofollow" data-drupal-facet-item-id="release-date-year-2018" data-drupal-facet-item-value="2018" data-drupal-facet-item-count="2"><span class="facet-item__value c-facet-summary__value">2018</span>
</a>
                                  </li></ul>


</div>

  </div>
</div>
  
  
  
  </div>






  <div  class="facet-inactive hidden block-facet--searchbox-checkbox c-block c-block--facet-block c-block--provider-facets c-block--id-facet-blockvendor">

  
  
    

  
      


<div  class="c-facet-block">
      <button class="c-facet-block__trigger" aria-expanded="false">
      <h3 class="c-facet-block__title">Vendor</h3>
    </button>
    <div class="c-facet-block__content" aria-hidden="true">
    
<div data-drupal-facet-id="vendor" class="facet-empty facet-hidden"><div class="facets-widget-searchbox_checkbox">
  <input type="text" placeholder="Search..." class="facets-widget-searchbox" data-type="checkbox" />
      
<div class="facets-widget-searchbox-no-result hide">No result</div>
</div>
</div>

  </div>
</div>
  
  
  
  </div>

      <a href="https://www.cisa.gov/news-events/cybersecurity-advisories" class="c-button c-button--small c-button--reset" hidden>Reset</a>
          </aside>
    
    <div class="l-sidebar__main">
              





  <div  class="views-element-container c-block c-block--view c-block--provider-views c-block--id-views-blockindex-advisory-listing-block-1">

  
  
    

      <div  class="c-block__content">
  
  
          <h1>Cybersecurity Alerts &amp; Advisories</h1>
    
          

<div  class="l-page-section">
  
  
  <div class="l-page-section__content">
          <p><a href="/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94" title="Cybersecurity Advisories">View Cybersecurity Advisories Only</a><br /><a href="#definitions" title="Advisory Definitions">View Advisory Definitions</a></p>
      </div>

  
  </div>
    
    


<div  class="c-view c-view--index-advisory-listing c-view--display-block_1 view js-view-dom-id-13f831818894d2bd2e2c6519b0ed1961b1b007d04f5187cc0be415de736f0ed3">
  
  
  

      <div class="c-view__header">





  <div  data-drupal-facets-summary-id="advisory_listing_summary" id="block-advisorylistingsummary" class="c-block c-block--provider-facets-summary c-block--id-facets-summary-blockadvisory-listing-summary">

  
  
    

      <div  class="c-block__content">
  
      <div class="c-facet-summary facets-widget-">
    <span class="c-facet-summary__label">
        Filters:
      </span>
      <ul class="c-facet-summary__list"><li class="facet-summary-item--facet c-facet-summary__item"><a href="/news-events/cybersecurity-advisories" rel="nofollow">  <span class="facet-item__status c-facet-summary__status js-facet-deactivate">(-)</span>
<span class="facet-item__value c-facet-summary__value">Cybersecurity Advisory</span>
</a></li><li class="facet-summary-item--clear c-facet-summary__item"><a href="/news-events/cybersecurity-advisories?page=13">Clear all filters</a></li></ul>

</div>

  
      </div>
  
  
  </div>
</div>
  
  
  


<div  class="c-view c-view--index-advisory-listing c-view--display-attachment_1 view js-view-dom-id-224054551b18780f775fac331e29fb54d0f245525e5ac976281bc079d3b9b7ab">
  
  
  

  
  
  

  
  
  
  

  
  
</div>



  

  

      <div  class="c-view__row">





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2019-06-17T12:00:00Z">Jun 17, 2019</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA19-168A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa19-168a" target="_self">          
<span>Microsoft Operating Systems BlueKeep Vulnerability</span>

        </a>      </h3>
                            </div>
  </div>
</article>

</div>
        <div  class="c-view__row">





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2019-05-02T12:00:00Z">May 02, 2019</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA19-122A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa19-122a" target="_self">          
<span>New Exploits for Unsecure SAP Systems</span>

        </a>      </h3>
                            </div>
  </div>
</article>

</div>
        <div  class="c-view__row">





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2019-01-24T12:00:00Z">Jan 24, 2019</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA19-024A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa19-024a" target="_self">          
<span>DNS Infrastructure Hijacking Campaign</span>

        </a>      </h3>
                            </div>
  </div>
</article>

</div>
        <div  class="c-view__row">





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2018-12-03T12:00:00Z">Dec 03, 2018</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA18-337A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa18-337a" target="_self">          
<span>SamSam Ransomware</span>

        </a>      </h3>
                            </div>
  </div>
</article>

</div>
        <div  class="c-view__row">





<article  class="is-promoted c-teaser c-teaser--horizontal" role="article">
  <div class="c-teaser__row">
        <div class="c-teaser__content">
              <div class="c-teaser__eyebrow">
                      <div class="c-teaser__date"><time datetime="2018-10-11T12:00:00Z">Oct 11, 2018</time>
</div>
                                <div class="c-teaser__meta">Cybersecurity Advisory | AA18-284A</div>
                  </div>
            <h3 class="c-teaser__title">
        <a href="/news-events/cybersecurity-advisories/aa18-284a" target="_self">          
<span>Publicly Available Tools Seen in Cyber Incidents Worldwide</span>

        </a>      </h3>
                            </div>
  </div>
</article>

</div>
  
    
  <nav  class="c-pager" role="navigation">
    <ul class="c-pager__items js-pager__items">
                            <li class="c-pager__item c-pager__item--first">
          <a class="c-pager__link c-pager__link--first" href="?f%5B0%5D=advisory_type%3A94&amp;page=0" aria-label="Go to first page" title="Go to first page" ><svg  class="c-icon c-icon--pager is-spaced-after" role="img" aria-hidden="true"><use xlink:href="/profiles/cisad8_gov/themes/custom/gesso/dist/images/sprite.artifact.svg#angle-double-left"></use></svg><span class="u-visually-hidden">Go to first page</span><span aria-hidden="true">First</span></a>
        </li>
      
                            <li class="c-pager__item c-pager__item--previous">
          <a class="c-pager__link c-pager__link--previous" href="?f%5B0%5D=advisory_type%3A94&amp;page=12" aria-label="Go to previous page" title="Go to previous page" rel="prev" ><svg  class="c-icon c-icon--pager is-spaced-after" role="img" aria-hidden="true"><use xlink:href="/profiles/cisad8_gov/themes/custom/gesso/dist/images/sprite.artifact.svg#angle-left"></use></svg><span class="u-visually-hidden">Go to previous page</span><span aria-hidden="true">Previous</span></a>
        </li>
      
                    <li class="c-pager__item c-pager__item--ellipsis" role="presentation">…</li>
      
                    <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=5" aria-label="Go to page 6" title="Go to page 6" >
              <span class="u-visually-hidden">
                Page
              </span>6</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=6" aria-label="Go to page 7" title="Go to page 7" >
              <span class="u-visually-hidden">
                Page
              </span>7</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=7" aria-label="Go to page 8" title="Go to page 8" >
              <span class="u-visually-hidden">
                Page
              </span>8</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=8" aria-label="Go to page 9" title="Go to page 9" >
              <span class="u-visually-hidden">
                Page
              </span>9</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=9" aria-label="Go to page 10" title="Go to page 10" >
              <span class="u-visually-hidden">
                Page
              </span>10</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=10" aria-label="Go to page 11" title="Go to page 11" >
              <span class="u-visually-hidden">
                Page
              </span>11</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=11" aria-label="Go to page 12" title="Go to page 12" >
              <span class="u-visually-hidden">
                Page
              </span>12</a>
                  </li>
              <li class="c-pager__item">
                                  <a class="c-pager__link" href="?f%5B0%5D=advisory_type%3A94&amp;page=12" aria-label="Go to page 13" title="Go to page 13" >
              <span class="u-visually-hidden">
                Page
              </span>13</a>
                  </li>
              <li class="c-pager__item c-pager__item--current">
                      <span class="u-visually-hidden">
              Currently on page
            </span>14        </li>
      
            
            
            
    </ul>
  </nav>

  
  

  
  
</div>


  
      </div>
  
  
  </div>






  <div  class="c-block c-block--provider-block-content c-block--id-block-content442f8564-d8d7-4a59-85a6-77cb8796a44b">

  
  
      <h2  class="c-block__title">Advisory Definitions</h2>
    

      <div  class="c-block__content">
  
      




<div  class="c-field c-field--name-body c-field--type-text-with-summary c-field--label-hidden">
  <div class="c-field__content"><p id="definitions"><strong>Cybersecurity Advisory:</strong> In-depth reports covering a specific cybersecurity issue, often including threat actor tactics, techniques, and procedures; indicators of compromise; and mitigations.<br /><strong>Alert: </strong>Concise summaries covering cybersecurity topics, such as mitigations that vendors have published for vulnerabilities in their products.<br /><strong>ICS Advisory:</strong> Concise summaries covering industrial control system (ICS) cybersecurity topics, primarily focused on mitigations that ICS vendors have published for vulnerabilities in their products.<br /><strong>ICS Medical Advisory:</strong> Concise summaries covering ICS medical cybersecurity topics, primarily focused on mitigations that ICS medical vendors have published for vulnerabilities in their products.<br /><strong>Analysis Report:</strong> In-depth analysis of a new or evolving cyber threat, including technical details and remediations.</p></div></div>

  
      </div>
  
  
  </div>

          </div>

      </div>

  </div>

  <div class="layout layout--twocol-section layout--twocol-section--33-67">

    
    
  </div>

  
  
  
  

      </div>

  
  </main>

  

<footer  class="usa-footer usa-footer--slim" role="contentinfo">
    <div class="usa-footer__return-to-top">
    <div class="l-constrain">
      <a href="#">Return to top</a>
    </div>
  </div>
    <div class="usa-footer__upper">
    <div class="l-constrain">
      







  
  
    

  
            

                                <ul  class="c-menu c-menu--footer-main">
        
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/topics" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7329">Topics</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/spotlight" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7330">Spotlight</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/resources-tools" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7331">Resources &amp; Tools</a>
                        </li>
    
                                            
                                                    
      
      
      <li  class="c-menu__item is-active-trail">
                              <a href="/news-events" class="c-menu__link js-top-level is-active-trail" aria-current="false" data-drupal-link-system-path="node/7332">News &amp; Events</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/careers" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/7323">Careers</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/about" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="node/6944">About</a>
                        </li>
        </ul>
  
    </div>
  </div>
    <div class="usa-footer__main">
    <div class="l-constrain">
      <div class="usa-footer__main-row">
        <div class="usa-footer__brand">
          
<a  class="c-site-name c-site-name--footer" href="/" rel="home" title="Go to the Cybersecurity & Infrastructure Security Agency homepage">
  <span class="c-site-name__text">Cybersecurity &amp; Infrastructure Security Agency</span>
</a>        </div>
        <div class="usa-footer__contact">
                      

                                <ul  class="c-menu c-menu--social">
        
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.facebook.com/CISA" class="c-menu__link--facebook c-menu__link js-top-level" aria-current="false">Facebook</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://twitter.com/CISAgov" class="c-menu__link--twitter c-menu__link js-top-level" aria-current="false">Twitter</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.linkedin.com/company/cybersecurity-and-infrastructure-security-agency" class="c-menu__link--linkedin c-menu__link js-top-level" aria-current="false">LinkedIn</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.youtube.com/@cisagov" class="c-menu__link--youtube c-menu__link js-top-level" aria-current="false">YouTube</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="https://www.instagram.com/cisagov" class="c-menu__link--instagram c-menu__link js-top-level" aria-current="false">Instagram</a>
                        </li>
    
                                            
                                                            
      
      
      <li  class="c-menu__item">
                              <a href="/subscribe-updates-cisa" class="c-menu__link--rss c-menu__link js-top-level" aria-current="false">RSS</a>
                        </li>
        </ul>
  

                    <div class="usa-footer__contact-info">
            <span>CISA Central</span>
            <a href="tel:8882820870">888-282-0870</a>
            <a href="mailto:central@cisa.dhs.gov">Central@cisa.dhs.gov</a>
          </div>
        </div>
      </div>
    </div>
  </div>
    <div class="usa-footer__lower">
    <div class="l-constrain">
      <div class="usa-footer__lower-row">
        <div class="usa-footer__lower-left">
          
<div  class="c-dhs-logo">
  <div class="c-dhs-logo__seal">DHS Seal</div>
  <div class="c-dhs-logo__content">
    <div class="c-dhs-logo__url">CISA.gov</div>
    <div class="c-dhs-logo__text">An official website of the U.S. Department of Homeland Security</div>
  </div>
</div>                      


                                <ul  class="c-menu c-menu--footer">
        
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/about" class="c-menu__link js-top-level" title="About CISA" aria-current="false" data-drupal-link-system-path="node/6944">About CISA</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov/accessibility" class="c-menu__link js-top-level" title="Accessibility" aria-current="false">Accessibility</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov/performance-financial-reports" class="c-menu__link js-top-level" title="Budget and Performance" aria-current="false">Budget and Performance</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov" title="Department of Homeland Security" class="c-menu__link js-top-level" aria-current="false">DHS.gov</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.dhs.gov/foia" class="c-menu__link js-top-level" title="FOIA Requests" aria-current="false">FOIA Requests</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/cisa-no-fear-act-reporting" title="No FEAR Act Reporting" class="c-menu__link js-top-level" aria-current="false">No FEAR Act</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.oig.dhs.gov/" class="c-menu__link js-top-level" title="Office of Inspector General" aria-current="false">Office of Inspector General</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/privacy-policy" class="c-menu__link js-top-level" title="Privacy Policy" aria-current="false" data-drupal-link-system-path="node/16115">Privacy Policy</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://public.govdelivery.com/accounts/USDHSCISA/subscriber/new?topic_id=USDHSCISA_138" title="Subscribe to Email Updates" class="c-menu__link js-top-level" aria-current="false">Subscribe</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.whitehouse.gov/" class="c-menu__link js-top-level" title="The White House" aria-current="false">The White House</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="https://www.usa.gov/" class="c-menu__link js-top-level" title="USA.gov" aria-current="false">USA.gov</a>
                        </li>
    
                                            
                              
      
      
      <li  class="c-menu__item">
                              <a href="/forms/feedback" title="Website Feedback" class="c-menu__link js-top-level" aria-current="false" data-drupal-link-system-path="forms/feedback">Website Feedback</a>
                        </li>
        </ul>
  

                  </div>
        <div class="usa-footer__lower-right">
          <iframe
            src="https://www.dhs.gov/ntas/"
            name="National Terrorism Advisory System"
            title="National Terrorism Advisory System"
            width="170"
            height="180"
            scrolling="no"
            frameborder="0"
            seamless border="0"
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</footer>


</div>

  </div>

    
        <script type="application/json" data-drupal-selector="drupal-settings-json">{"path":{"baseUrl":"\/","scriptPath":null,"pathPrefix":"","currentPath":"node\/15842","currentPathIsAdmin":false,"isFront":false,"currentLanguage":"en","currentQuery":{"f":["advisory_type:94"],"page":"13"}},"pluralDelimiter":"\u0003","suppressDeprecationErrors":true,"google_analytics":{"account":"G-9MDR73GM0K","trackOutbound":true,"trackMailto":true,"trackTel":true,"trackDownload":true,"trackDownloadExtensions":"7z|aac|arc|arj|asf|asx|avi|bin|csv|doc(x|m)?|dot(x|m)?|exe|flv|gif|gz|gzip|hqx|jar|jpe?g|js|mp(2|3|4|e?g)|mov(ie)?|msi|msp|pdf|phps|png|ppt(x|m)?|pot(x|m)?|pps(x|m)?|ppam|sld(x|m)?|thmx|qtm?|ra(m|r)?|sea|sit|tar|tgz|torrent|txt|wav|wma|wmv|wpd|xls(x|m|b)?|xlt(x|m)|xlam|xml|z|zip"},"data":{"extlink":{"extTarget":false,"extTargetNoOverride":false,"extNofollow":false,"extNoreferrer":false,"extFollowNoOverride":false,"extClass":"ext","extLabel":"(link is external)","extImgClass":false,"extSubdomains":true,"extExclude":"(.\\.gov$)|(.\\.mil$)|(.\\.mil\/)|(.\\.gov\/)","extInclude":"","extCssExclude":".c-menu--social,.c-menu--footer,.c-social-links,.c-text-cta--button","extCssExplicit":"","extAlert":true,"extAlertText":"You are now leaving an official website of the United State Government (USG), the Department of Homeland Security (DHS) and the Cybersecurity and Infrastructure Security Agency (CISA). Links to non-USG, non-DHS and non-CISA sites are provided for the visitor\u0027s convenience and do not represent an endorsement by USG, DHS or CISA of any commercial or private issues, products or services. Note that the privacy policy of the linked site may differ from that of USG, DHS and CISA.","mailtoClass":"mailto","mailtoLabel":"(link sends email)","extUseFontAwesome":false,"extIconPlacement":"append","extFaLinkClasses":"fa fa-external-link","extFaMailtoClasses":"fa fa-envelope-o","whitelistedDomains":[]}},"ckeditorExpandableTextbox":{"accordionStyle":{"collapseAll":true,"keepRowsOpen":false}},"ckeditorAccordion":{"accordionStyle":{"collapseAll":1,"keepRowsOpen":0,"animateAccordionOpenAndClose":1,"openTabsWithHash":1}},"facets":{"softLimit":{"vendor":15},"softLimitSettings":{"vendor":{"showLessLabel":"Show less","showMoreLabel":"Show more"}}},"ajaxTrustedUrl":{"\/news-events\/cybersecurity-advisories":true},"facets_views_ajax":{"facets_summary_ajax":{"facets_summary_id":"advisory_listing_summary","view_id":"index_advisory_listing","current_display_id":"block_1","ajax_path":"\/views\/ajax"}},"user":{"uid":0,"permissionsHash":"2e28e3d4cecae698758a87360e5c783a3a6bbf12a454265e787234af3fdfaba5"}}</script>
<script src="/core/assets/vendor/jquery/jquery.min.js?v=3.7.0"></script>
<script src="/core/assets/vendor/once/once.min.js?v=1.0.1"></script>
<script src="/core/misc/drupalSettingsLoader.js?v=10.1.5"></script>
<script src="/core/misc/drupal.js?v=10.1.5"></script>
<script src="/core/misc/drupal.init.js?v=10.1.5"></script>
<script src="/modules/contrib/google_analytics/js/google_analytics.js?v=10.1.5"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/common.js?s4w5q2"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/uswds-init.es6.js?s4w5q2"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/uswds.es6.js?s4w5q2"></script>
<script src="https://dap.digitalgov.gov/Universal-Federated-Analytics-Min.js?" id="_fed_an_ua_tag"></script>
<script src="/modules/contrib/extlink/extlink.js?v=10.1.5"></script>
<script src="/profiles/cisad8_gov/modules/custom/cisa_core/js/ckeditor-expandabletextbox.js?v=1.1.x"></script>
<script src="/modules/contrib/ckeditor_accordion/js/accordion.frontend.js?s4w5q2"></script>
<script src="/modules/contrib/facets/js/base-widget.js?v=10.1.5"></script>
<script src="/modules/contrib/facets/js/checkbox-widget.js?v=10.1.5"></script>
<script src="/modules/contrib/facets/modules/facets_searchbox_widget/js/searchbox.js?v=10.1.5" defer></script>
<script src="/modules/contrib/facets/js/soft-limit.js?v=10.1.5"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/facet-block.es6.js?s4w5q2"></script>
<script src="/profiles/cisad8_gov/themes/custom/gesso/dist/js/teaser.es6.js?s4w5q2"></script>

  </body>
</html>

"""
class DetailSection: 
    section = ''
    content = ''
    def __init__(self, section, content):
        self.section = section
        self.content = content
    
    def __str__(self):
        return self.section + '\n' + self.content

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert First HTML table in file to CSV')
    
    parser.add_argument('-a', '--address', help='base web address', required=True)
    parser.add_argument('-p', '--maxpages', help='The Maximum number of pages', required=True)
    parser.add_argument('-b', '--baseurl', help='The baseurl', required=True)
    args = parser.parse_args()

    # html download
    # TODO: add download



    soup = BeautifulSoup(html, 'html.parser')
    alerts_items = soup.find_all('h3', class_='c-teaser__title')
    

    for item in alerts_items:
        print(item.find('span').get_text())
        print(argparse.baseurl + '/' + item.find('a').get('href'))

    # download the alert
    # TODO: download the alert
    soup2 = BeautifulSoup(html2, 'html.parser')
    content = soup2.find('main')
    title = re.sub(r'\n\s*\n', r'\n\n', content.find('h1').get_text().strip(), flags=re.M)
    date = re.sub(r'\n\s*\n', r'\n\n', content.find('time')['datetime'], flags=re.M)
    alert_cd = re.sub(r'\n\s*\n', r'\n\n', content.find('div', class_='c-field--name-field-alert-code').find('div', class_='c-field__content').get_text().strip(), flags=re.M)


    print(title)
    print(date)
    print(alert_cd)
    subcontent = content.find('div', class_="l-page-section__content")
    fullbody = re.sub(r'\n\s*\n', r'\n\n', subcontent.get_text().strip(), flags=re.M)
    arrayObj = []
    currObj = DetailSection('','')
    for sc in subcontent.contents:
        if sc.find('h3') and sc.get_text().strip() != '':
            heading=sc.get_text().strip()
            section = re.sub(r'\n\s*\n', r'\n\n', heading, flags=re.M)
            if currObj:
                arrayObj.append(currObj)
                currObj = DetailSection('','')
            currObj.section = section
            currObj.content = ''
        else:
            currObj.content += ' ' + re.sub(r'\n\s*\n', r'\n\n', sc.get_text().strip(), flags=re.M)
    arrayObj.append(currObj)

    print(arrayObj[2].section)
    print(arrayObj[2].content)

    
