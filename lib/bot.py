from murasaki import Murasaki
from settings import MURASAKI_USER, MURASAKI_PASSWORD

def parse_unit(transitionUnit):
    s = transitionUnit
    s = s.replace("(", ", ").replace(")", "")
    if "," in s:
        name, unit = s.split(",")
        name = name.lower().strip()
        unit = unit.strip()

    else:
        name = s.lower()
        unit = None

    return {
        "Name": name,
        "Unit": unit,
    } 

def determine_development(change, stable_threshold=0.01):
    if abs(change) <= stable_threshold:
        return "stable"
    elif change > 0:
        return "increase"
    elif change < 0:
        return "decrease"

def more_or_less(diff, same_level_threshold=0.01):
    if abs(diff) <= same_level_threshold:
        return "same"
    elif diff > 0:
        return "more"
    elif diff < 0:
        return "less"


def generate_summary(now, then):
    murasaki_api = Murasaki("https://jplusplus-murasaki.herokuapp.com/",
                            user=MURASAKI_USER, password=MURASAKI_PASSWORD)

    context = {
        "Now": now,
        "Then": then,
    }

    context["Unit"] = parse_unit(now["transitionUnit"])
    context["Now"]["vsTarget"] = more_or_less(now["targetDiffPct"])

    try:
        context["ChangePct"] = now["outcomeLatestValue"] / then["outcomeLatestValue"] - 1
        context["Dev"] = more_or_less(context["ChangePct"])
        context["Then"]["vsTarget"] = more_or_less(then["targetDiffPct"])

    except ZeroDivisionError:
        context["ChangePct"] = None
        context["Dev"] = more_or_less(now["outcomeLatestValue"])
    
    except TypeError:
        # outcomeLatestValue är None
        context["ChangePct"] = None
        context["Dev"] = None
    
    template = """
- const StableThreshold = 0.01
- const överEllerUnder = diff => diff > 0 ? "över" : "under"

p Datauppdatering på Panorama!

hr

p Det har kommit nya siffror om <strong>#{ Now.title.toLowerCase() }</strong> för <strong>#{ Math.round(Now.outcomeLatestYear) }</strong>. 

p Det mått som följs upp är <strong>#{ Unit.Name }</strong> (mätt i #{ Unit.Unit }).

hr

h3 Hur ligger vi till?

p Här är vi: #{ number( Now.outcomeLatestValue ) } #{ Unit.Unit }
p Vi borde vara på: #{ number( Now.targetLatestValue ) } #{ Unit.Unit }
p Vi ligger alltså 
    strong
        if Now.vsTarget == "same"
            | ungefär där vi borde vara

        else if Now.vsTarget == "less"
            | sämre än målet 😢

        else if Now.vsTarget == "more"
            | bättre än målet 😊
    |.  


if Then.vsTarget        
    hr

    h3 Vartåt pekar utvecklingen?

    p 
        | År #{ Math.round(Then.outcomeLatestYear) } låg vi 

        if Then.vsTarget == "same"
            | i linje med målbanan,  

        else if Then.vsTarget == "less"
            | #{ percent(Math.abs(Then.targetDiffPct)) } procent under målbanan, 

        else if Then.vsTarget == "more"
            | #{ percent(Then.targetDiffPct) } procent över målbanan, 

        else
            | ERROR: #{Then.vsTarget}
                
        
        | i dag ligger vi  
        if Now.vsTarget == "same"
            | i linje.  

        else if Now.vsTarget == "less"
            | #{ percent(Math.abs(Now.targetDiffPct)) } procent under. 

        else if Now.vsTarget == "more"
            | #{ percent(Now.targetDiffPct) } procent över. 

        
        if Math.abs(Now.targetDiffPct - Then.targetDiffPct) > 0.01
            | Utvecklingen går alltså åt 
            strong
                if Now.targetDiffPct > Then.targetDiffPct
                    | rätt håll 😊
                
                else
                    | fel håll 😢

            |. 

hr

h3 Hur avgörande är den här indikatorn?

p #{ Now.title } står i Panoramas scenario för <strong>#{ percent(Now.co2e / 47.75) } procent</strong> av utsläppsminskningen.  
        
p
    a(href=`https://app.climateview.global/v3/public/board/ec2d0cdf-e70e-43fb-85cb-ed6b31ee1e09?id=${Now.id}`)
        | Läs mer om den här indikatorn på Panorama.

    """

    return murasaki_api.pug(context, template) 