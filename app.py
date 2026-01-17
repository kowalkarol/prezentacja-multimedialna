import streamlit as st
import streamlit.components.v1 as components
import json
import os


# --- Custom Timeline Component (z obsługą Dark Mode) ---
def timeline(data, height=600):
    """
    Customowa wersja timeline'u z detekcją motywu Streamlit (JS).
    """
    if isinstance(data, str):
        data = json.loads(data)

    # Serializacja danych do JSON
    json_text = json.dumps(data)
    source_param = "timeline_json"
    source_block = f"var {source_param} = {json_text};"

    # Zasoby TimelineJS
    cdn_path = "https://cdn.knightlab.com/libs/timeline3/latest"

    # CSS - Klasa .dark-mode aktywowana przez JS
    custom_css = """
    <style>
        /* Styl dla trybu ciemnego (aktywowany klasą body.dark-mode) */
        body.dark-mode .tl-timeline {
            filter: invert(100%) hue-rotate(180deg);
            background-color: #ffffff;
        }
        
        body.dark-mode img, 
        body.dark-mode video, 
        body.dark-mode iframe {
            filter: invert(100%) hue-rotate(180deg) !important;
        }
        
        body.dark-mode .tl-slide-content {
            background-color: #fff !important; 
        }
    </style>
    """

    css_block = f'<link title="timeline-styles" rel="stylesheet" href="{cdn_path}/css/timeline.css">'
    js_block = f'<script src="{cdn_path}/js/timeline.js"></script>'

    # Skrypt detekcji motywu z rodzica (Streamlit)
    theme_detection_js = r"""
    <script>
        function updateTheme() {
            try {
                // Próba odczytu motywu z ramki nadrzędnej (aplikacji Streamlit)
                // Wymaga uruchomienia na tym samym originie (zazwyczaj localhost działa)
                var theme = "light";
                var parentDoc = window.parent.document;
                
                if (parentDoc) {
                    // Metoda: Sprawdzenie koloru tła (bardziej niezawodne)
                    var style = window.getComputedStyle(parentDoc.body);
                    var bg = style.backgroundColor;
                    
                    if (bg && bg.includes('rgb')) {
                        var rgb = bg.match(/\d+/g).map(Number);
                        // Luminancja < 128 = Ciemny
                        var luma = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2];
                        if (luma < 128) theme = 'dark';
                        else theme = 'light';
                    }
                }
                
                if (theme === 'dark') {
                    document.body.classList.add('dark-mode');
                } else {
                    document.body.classList.remove('dark-mode');
                }
                
            } catch (e) {
                // Fallback do preferencji systemowych w razie błędu CORS/Sandbox
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                     document.body.classList.add('dark-mode');
                }
            }
        }
        
        // Uruchom przy starcie
        updateTheme();
        // Sprawdzaj cyklicznie (reakcja na przełącznik w menu)
        setInterval(updateTheme, 500);
    </script>
    """

    # Złożenie HTML
    htmlcode = f"""
    {css_block}
    {custom_css}
    {js_block}
    <div id='timeline-embed' style="width: 100%; height: {height}px; margin: 0px;"></div>
    <script type="text/javascript">
        var additionalOptions = {{
            start_at_end: false, 
            is_embed: false,
            timenav_height_min: 150
        }}
        {source_block}
        window.timeline = new TL.Timeline('timeline-embed', {source_param}, additionalOptions);
    </script>
    {theme_detection_js}
    """

    return components.html(htmlcode, height=height)


# Konfiguracja Strony
st.set_page_config(
    page_title="Ewolucja Generowania Wideo AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Sidebar: Legenda i Info ---
def render_sidebar():
    st.sidebar.title("📖 Legenda Techniczna")
    st.sidebar.markdown("---")

    st.sidebar.subheader("Architektury")
    st.sidebar.markdown(
        """
    **GAN (Generatywna Sieć Przeciwnicza):**
    Dwie sieci neuronowe (Generator kontra Dyskryminator) rywalizują ze sobą. Generator tworzy dane, a Dyskryminator je ocenia. Dominująca technologia w latach 2014-2020.
    
    **VAE (Wariacyjny Autoenkoder):**
    Koduje dane wejściowe do rozkładu ukrytego (latent) i dekoduje je z powrotem. Dobry do zachowania struktury, ale często daje rozmyte wyniki w porównaniu do GAN.
    
    **Autoregresyjne Transformery:**
    Przewidują kolejny token (piksel lub fragment ukryty) w sekwencji. Zaadaptowane z NLP (styl GPT) do obrazów i wideo.
    
    **Modele Dyfuzyjne (Diffusion Models):**
    Uczą się odwracać proces zaszumiania. Zaczynają od czystego szumu i iteracyjnie udoskonalają go w obraz/wideo. Obecny stan wiedzy (SOTA).
    """
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Kluczowe Pojęcia")
    st.sidebar.markdown(
        """
    *   **Spójność Czasowa (Temporal Consistency):** Zdolność do utrzymania stabilności obiektów między klatkami bez migotania.
    *   **Uwaga Czasoprzestrzenna (Spatiotemporal Attention):** Mechanizmy uwagi stosowane jednocześnie w wymiarze przestrzeni (obraz) i czasu (sekwencja).
    *   **Przestrzeń Ukryta (Latent Space):** Skompresowana reprezentacja danych, na której operuje model, aby oszczędzać moc obliczeniową.
    """
    )


# --- GENEROWANIE DANYCH (Rdzeń) ---
def get_timeline_data():
    """
    Zwraca słownik wymagany przez TimelineJS.
    Wczytuje dane z pliku zewnętrznego timeline_data.json
    """
    try:
        with open("timeline_data.json", "r", encoding="utf-8") as f:
            events = json.load(f)
        return {"events": events}
    except FileNotFoundError:
        st.error("Nie znaleziono pliku timeline_data.json!")
        return {"events": []}
    except json.JSONDecodeError as e:
        st.error(f"Błąd parsowania pliku JSON: {e}")
        return {"events": []}


# --- Główna Logika Aplikacji ---
def main():
    render_sidebar()

    st.title("Ewolucja Generowania Wideo AI")
    st.markdown("### Techniczna Oś Czasu: Od GAN do Modeli Świata (2014-2024)")
    st.markdown(
        """
    Ta interaktywna oś czasu obrazuje wykładniczy postęp generatywnych modeli wideo. 
    Od rozmytych, czarno-białych wyników wczesnych **GAN-ów**, przez rozłączne reprezentacje **MoCoGAN**, 
    aż po fotorealistyczne, symulujące fizykę **Transformery Dyfuzyjne** (Sora, Kling, Gen-3) dzisiejszych czasów.
    """
    )

    # Załadowanie Danych
    data = get_timeline_data()

    # Wyświetlenie osi czasu (TimelineJS)
    if data["events"]:
        timeline(data, height=800)

    # --- Sekcja Szczegółów Technicznych (Rozwijana) ---
    st.markdown("## 🔍 Szczegółowa Analiza: Trendy Techniczne w Epokach")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("2014-2018: Era GAN", expanded=True):
            st.markdown(
                """
            **Dominująca Architektura:** GAN (cGAN, VGAN, Progressive GAN).
            
            **Wyzwania:**
            *   **Zapadanie się modów (Mode Collapse):** Modele generowały tylko jeden typ wyniku.
            *   **Niestabilność Treningu:** Dyskryminator zazwyczaj zbyt szybko przewyższał Generator.
            *   **Migotanie:** Brak zrozumienia czasu; każda klatka generowana niemal niezależnie lub ze słabymi ograniczeniami przepływu optycznego.
            
            **Kamień Milowy:** Oddzielenie Treści (co) od Ruchu (gdzie).
            """
            )

    with col2:
        with st.expander("2019-2022: Transformery i Wczesna Dyfuzja", expanded=False):
            st.markdown(
                """
            **Dominująca Architektura:** VQ-VAE + Transformery (GODIVA, NÜWA), Wczesna Dyfuzja (Make-A-Video).
            
            **Zmiana:**
            *   Przejście od generowania pikseli bezpośrednio do generowania **Tokenów** w przestrzeni ukrytej (latent).
            *   **Text-to-Video:** Wprowadzenie CLIP pozwoliło modelom rozumieć prompty w języku naturalnym.
            *   **Zero-Shot:** Zastosowanie modeli dyfuzji obrazu do wideo poprzez "hakowanie" warstw uwagi.
            """
            )

    with col3:
        with st.expander("2023-Obecnie: Transformery Dyfuzyjne (DiT)", expanded=False):
            st.markdown(
                """
            **Dominująca Architektura:** Space-Time U-Net (Lumiere), DiT (Sora, Gen-3).
            
            **Obecny Stan:**
            *   **Modele Świata:** Modele nie tylko wklejają piksele; symulują fizykę 3D, oświetlenie i trwałość obiektów.
            *   **Prawa Skalowania:** Więcej obliczeń + więcej danych = wyłaniające się zrozumienie fizycznego świata.
            *   **Natywny Czas:** Przetwarzanie całej objętości wideo naraz (Lumiere) zamiast klatka po klatce.
            """
            )

    st.markdown("---")
    st.info(
        "Instrukcja: Przewijaj poziomo oś czasu lub klikaj daty na dole, aby nawigować."
    )


if __name__ == "__main__":
    main()
