import streamlit as st
import pandas as pd

import model.braquages
from farwest.model.attitudes import Attitude

st.title('le tournoi du far-west')
st.subheader('à défaut de cow-boys')


nombre_equipes = st.slider("nombre d'équipes", min_value=2, max_value=5, value=3, step=None, format=None,
                           key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

nombre_de_braquages = st.slider("nombre de braquages", min_value=20, max_value=200, value=200, step=20, format=None,
                                key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

gain_seul = st.slider("gain si on braque la banque seul", min_value=1000, max_value=20000, value=10000, step=1000,
                      format=None,
                      key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

gain_a_deux = st.slider("gain du braquage si on braque la banque à deux équipes (et donc à diviser par deux)", min_value=1000, max_value=20000, value=14000,
                        step=1000, format=None,
                        key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

show_graphs = st.radio("voir les graphes", options=['oui', 'non'], index=1, key=None,
                       help=None, on_change=None, args=None, kwargs=None, disabled=False, horizontal=False)

cols = list(st.columns(nombre_equipes))


def make_attitude(index):
    with cols[index]:
        label = f"équipe {index}"
        option = st.selectbox(
            f"attitude de {label}: ",
            list(map(lambda e: e.name, Attitude)))
    return [label, option]


attitudes = list(map(make_attitude, range(nombre_equipes)))


def simulate():
    data = []
    for indexA in range(nombre_equipes):
        for indexB in range(indexA + 1, nombre_equipes):
            attitudeA = Attitude[attitudes[indexA][1]]
            attitudeB = Attitude[attitudes[indexB][1]]
            df = model.braquages.make_campagne(nombre_de_braquages=nombre_de_braquages, gain_seul=gain_seul,
                                               gain_a_deux=gain_a_deux, a1=attitudeA, a2=attitudeB)
            chart_data = df[["gains A", "gains B"]]
            label = f"équipe {indexA} ({attitudeA.name}) contre équipe {indexB} ({attitudeB.name})"
            if show_graphs == 'oui':
                st.header(label)
                st.line_chart(chart_data)
            gainsA = df["gains A"].sum()
            gainsB = df["gains B"].sum()
            data.append([f"équipe {indexA} ({attitudeA.name})", f"équipe {indexB} ({attitudeB.name})", gainsA, gainsB])

    st.header("resultat des braquages par paire d'équipes")
    st.text(f"le maximum est {nombre_de_braquages} (braquages) * {gain_seul} (gain seul) : {nombre_de_braquages*gain_seul}")
    dfgains = pd.DataFrame(columns=["A", "B", "gains A", "gains B"], data=data)
    dfgains = dfgains.astype({"gains A":"int32","gains B":"int32"})
    print(dfgains)
    st.dataframe(data=dfgains)

    dfalla = dfgains[["A", "gains A"]].rename(columns={"A": "équipe", "gains A": "gains"})
    #st.dataframe(data=dfalla)
    dfallb = dfgains[["B", "gains B"]].rename(columns={"B": "équipe", "gains B": "gains"})
    #st.dataframe(data=dfallb)
    dfall = dfalla
    dfall = dfall.append(dfallb)
    #st.dataframe(data=dfall)

    dfall = dfall.groupby("équipe")['gains'].aggregate("sum")
    dfall=dfall.astype({"gains":'int32'})
    st.header("resultat des gains")
    nbpairs = nombre_equipes-1
    st.text(f"le maximum est {nombre_de_braquages} (braquages) * {gain_seul} (gain seul) * {nbpairs} (nombre de paires par équipe) \n: {nombre_de_braquages*gain_seul*nbpairs}")
    st.dataframe(data=dfall)


st.button("GO !", key=None, help=None, on_click=simulate, args=None, kwargs=None, disabled=False)

