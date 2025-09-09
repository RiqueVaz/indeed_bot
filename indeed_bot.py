"""
Indeed Auto-Apply Bot
---------------------
Automates job applications on Indeed using Camoufox.

Usage:
  - Configure your search and Chrome settings in config.yaml
  - Run: python indeed_bot.py

Author: @meteor314 
License: MIT
"""
import yaml
import time
from datetime import datetime
from typing import Dict, Any
from camoufox.sync_api import Camoufox
import logging


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
camoufox_config = config.get("camoufox", {})
user_data_dir = camoufox_config.get("user_data_dir")
language = camoufox_config.get("language")


def collect_indeed_apply_links(page, language):
    """Collect all 'Indeed Apply' job links from the current search result page."""
    links = []
    job_cards = page.query_selector_all('div[data-testid="slider_item"]')
    for card in job_cards:
        indeed_apply = card.query_selector('[data-testid="indeedApply"]')
        if indeed_apply:
            link = card.query_selector('a.jcs-JobTitle')
            if link:
                job_url = link.get_attribute('href')
                if job_url:
                    if job_url.startswith('/'):
                        job_url = f"https://{language}.indeed.com{job_url}"
                    links.append(job_url)
    return links


def click_and_wait(element, timeout=5):
    if element:
        element.click()
        time.sleep(timeout)


def apply_to_job(browser, job_url, language, logger):
    """Open a new tab, apply to the job, log the result, and close the tab."""
    page = browser.new_page()
    try:
        page.goto(job_url)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        # Step 1: Click the Indeed Apply button using XPath
        apply_btn = page.query_selector('xpath=//*[@id="indeedApplyButton"]')
        if not apply_btn:
            logger.warning(f"Indeed Apply button not found for {job_url}")
            page.close()
            return False
        
        click_and_wait(apply_btn, 5)
        logger.info(f"Clicked Indeed Apply button for {job_url}")

        # Step 2: Loop through "Continuar" buttons until we find "Enviar sua candidatura"
        start_time = time.time()
        while True:
            if time.time() - start_time > 40:
                logger.warning(f"Timeout applying to {job_url}, closing tab and moving to next.")
                break
            
            # Check if we have the "return to search" button (success indicator)
            return_btn = page.query_selector('xpath=//*[@id="returnToSearchButton"]')
            if return_btn:
                logger.info(f"Successfully applied to {job_url} - return button found")
                break
            
            # Look for "Enviar sua candidatura" button
            submit_btn = None
            btns = page.query_selector_all('button:visible')
            for btn in btns:
                text = (btn.inner_text() or "").strip()
                if "Enviar sua candidatura" in text:
                    submit_btn = btn
                    break
            
            if submit_btn:
                click_and_wait(submit_btn, 3)
                logger.info(f"Clicked 'Enviar sua candidatura' for {job_url}")
                time.sleep(2)  # Wait for the return button to appear
                continue
            
            # Look for "Continuar" button
            continue_btn = None
            for btn in btns:
                text = (btn.inner_text() or "").strip()
                if "Continuar" in text:
                    continue_btn = btn
                    break
            
            if continue_btn:
                click_and_wait(continue_btn, 3)
                logger.info(f"Clicked 'Continuar' for {job_url}")
                time.sleep(2)
            else:
                logger.warning(f"No 'Continuar' or 'Enviar sua candidatura' button found for {job_url}")
                break
        
        page.close()
        return True
        
    except Exception as e:
        logger.error(f"Error applying to {job_url}: {e}")
        page.close()
        return False


def setup_logger():
    logger = logging.getLogger("indeed_apply")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("indeed_apply.log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


with Camoufox(user_data_dir=user_data_dir,
              persistent_context=True) as browser:
    logger = setup_logger()
    page = browser.new_page()
    page.goto("https://" + language + ".indeed.com")

    cookies = page.context.cookies()
    ppid_cookie = next(
        (cookie for cookie in cookies if cookie['name'] == 'PPID'), None)
    if not ppid_cookie:
        print("Token não encontrado, por favor faça login no Indeed primeiro.")
        print("Redirecionando para página de login...")
        print("Você precisa reiniciar o bot após fazer login.")
        page.goto(
            "https://secure.indeed.com/auth?hl=" + language)
        time.sleep(1000)  # wait for manual login
    else:
        print("Token encontrado, prosseguindo com busca de vagas...")
        search_config = config.get("search", {})
        base_url = search_config.get("base_url", "")
        start = search_config.get("start", "")
        end = search_config.get("end", "")

        listURL = []
        i = start
        while i <= end:
            url = f"{base_url}&start={i}"
            listURL.append(url)
            i += 10

        all_job_links = []
        for url in listURL:
            print(f"Visitando URL: {url}")
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")
            print(
                "Aguardando página carregar, se aparecer algum botão de proteção Cloudflare... clique nele.")
            time.sleep(10)

            try:
                links = collect_indeed_apply_links(page, language)
                all_job_links.extend(links)
                print(f"Encontradas {len(links)} vagas Indeed Apply nesta página.")
            except Exception as e:
                print("Erro ao extrair vagas:", e)
            time.sleep(5)

        print(f"Total de vagas Indeed Apply encontradas: {len(all_job_links)}")
        for job_url in all_job_links:
            print(f"Candidatando-se a: {job_url}")
            success = apply_to_job(browser, job_url, language, logger)
            if not success:
                logger.error(f"Falha ao se candidatar a {job_url}")
            time.sleep(5)
        all_job_links = []
        for url in listURL:
            print(f"Visitando URL: {url}")
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(7)
            try:
                links = collect_indeed_apply_links(page, language)
                all_job_links.extend(links)
                print(f"Encontradas {len(links)} vagas Indeed Apply nesta página.")
            except Exception as e:
                print("Erro ao extrair vagas:", e)
            time.sleep(5)

        print(f"Total de vagas Indeed Apply encontradas: {len(all_job_links)}")
        for job_url in all_job_links:
            print(f"Candidatando-se a: {job_url}")
            success = apply_to_job(browser, job_url, language, logger)
            if not success:
                logger.error(f"Falha ao se candidatar a {job_url}")
            time.sleep(5)
