import os
import csv
from playwright.sync_api import sync_playwright

def scrape_match():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "valorant_stats.csv")
    user_data_dir = os.path.join(base_dir, "browser_session")

    player_totals = {}

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 720}
        )

        while True:
            match_id = input("\nEnter Match ID (or type 'exit' to finish and save): ").strip()
            if match_id.lower() == 'exit':
                break

            url = f"https://www.rib.gg/series/{match_id}"
            page = context.new_page()
            print(f"Navigating to {url}...")
            
            try:
                page.goto(url)
                page.wait_for_selector(".MuiTableBody-root", timeout=15000)
                
                rows = page.query_selector_all("tr.MuiTableRow-root")
                
                mk_data = {}
                mk_section = page.locator("div:has-text('Multikills and Clutches') + table")
                if mk_section.count() > 0:
                    mk_rows = mk_section.locator("tbody tr").all()
                    for mk_row in mk_rows:
                        mk_cells = mk_row.locator("td").all()
                        if len(mk_cells) >= 5:
                            p_name = mk_cells[0].inner_text().strip()
                            k3 = mk_cells[2].inner_text().strip() or "0"
                            k4 = mk_cells[3].inner_text().strip() or "0"
                            k5 = mk_cells[4].inner_text().strip() or "0"
                            mk_data[p_name] = {
                                "3k": int(k3) if k3.isdigit() else 0,
                                "4k": int(k4) if k4.isdigit() else 0,
                                "5k": int(k5) if k5.isdigit() else 0
                            }

                for row in rows:
                    cells = row.query_selector_all("td")
                    name_link = row.query_selector('a[href*="/players/"]')

                    if name_link and len(cells) >= 12:
                        name = name_link.inner_text().strip()
                        
                        def clean(val): 
                            val = val.replace('%', '').strip()
                            return float(val) if val and val != '-' else 0.0

                        rating = clean(cells[1].inner_text())
                        acs = clean(cells[2].inner_text())
                        
                        kda_box = cells[3].query_selector_all("div.css-viynl3")
                        kills = clean(kda_box[0].inner_text()) if len(kda_box) >= 3 else 0
                        deaths = clean(kda_box[1].inner_text()) if len(kda_box) >= 3 else 0
                        assists = clean(kda_box[2].inner_text()) if len(kda_box) >= 3 else 0

                        kast = clean(cells[11].inner_text())
                        adr = clean(cells[6].inner_text())
                        hs_p = clean(cells[12].inner_text())
                        fk = clean(cells[7].inner_text())
                        fd = clean(cells[8].inner_text())
                        
                        clutch_raw = cells[10].inner_text()
                        clutch = clean(clutch_raw.split('/')[0]) if '/' in clutch_raw else clean(clutch_raw)

                        player_mk = mk_data.get(name, {"3k": 0, "4k": 0, "5k": 0})

                        if name not in player_totals:
                            player_totals[name] = {
                                "matches": 0, "Rating": 0, "ACS": 0, "Kills": 0, "Deaths": 0, 
                                "Assists": 0, "KAST": 0, "ADR": 0, "HS%": 0, "FK": 0, "FD": 0, 
                                "Clutch": 0, "3k": 0, "4k": 0, "5k": 0
                            }
                        
                        p_stats = player_totals[name]
                        p_stats["matches"] += 1
                        p_stats["Rating"] += rating
                        p_stats["ACS"] += acs
                        p_stats["Kills"] += kills
                        p_stats["Deaths"] += deaths
                        p_stats["Assists"] += assists
                        p_stats["KAST"] += kast
                        p_stats["ADR"] += adr
                        p_stats["HS%"] += hs_p
                        p_stats["FK"] += fk
                        p_stats["FD"] += fd
                        p_stats["Clutch"] += clutch
                        p_stats["3k"] += player_mk["3k"]
                        p_stats["4k"] += player_mk["4k"]
                        p_stats["5k"] += player_mk["5k"]

                print(f"Stats processed for {match_id}.")

            except Exception as e:
                print(f"Error processing {match_id}: {e}")
            
            page.close()

        if player_totals:
            headers = ["Name", "Rating", "ACS", "Kills", "Deaths", "Assists", "KAST", "ADR", "HS%", "FK", "FD", "Clutch", "3k", "4k", "5k"]
            
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for name, stats in player_totals.items():
                    m_count = stats["matches"]
                    
                    row = [
                        name,
                        round(stats["Rating"] / m_count, 2),
                        round(stats["ACS"] / m_count, 1),
                        int(stats["Kills"]),
                        int(stats["Deaths"]),
                        int(stats["Assists"]),
                        round(stats["KAST"] / m_count, 1),
                        round(stats["ADR"] / m_count, 1),
                        round(stats["HS%"] / m_count, 1),
                        int(stats["FK"]),
                        int(stats["FD"]),
                        int(stats["Clutch"]),
                        stats["3k"],
                        stats["4k"],
                        stats["5k"]
                    ]
                    writer.writerow(row)
            
            print(f"\nSuccessfully saved combined stats for {len(player_totals)} unique players.")

        context.close()

if __name__ == "__main__":
    scrape_match()
