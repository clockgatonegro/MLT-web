import csv,json,collections,datetime
import networkx as nx
E=list(csv.DictReader(open('salida/exposiciones.csv')));A=list(csv.DictReader(open('salida/agentes.csv')));R=list(csv.DictReader(open('salida/aristas.csv')))
MOD={'individual':0,'colectiva':1,'n/d':2}
def dias(a,b):
    try:
        if len(a)==10 and len(b)==10:
            d=(datetime.date.fromisoformat(b)-datetime.date.fromisoformat(a)).days
            return d if 0<=d<=1500 else None
    except Exception: pass
    return None
idx={};nodes=[]
for e in E:
    idx[e['Id']]=len(nodes)
    src=e['fuente_url'] or ''
    nodes.append([e['Id'],e['Label'],0,int(e['ano']) if e['ano'] else None,e['fecha_ini'],e['fecha_fin'],e['espacio'],MOD[e['modalidad']],src,e['pieza_cactus'],e['tipo_expo'],dias(e['fecha_ini'],e['fecha_fin'])])
cl={'persona':1,'organizacion':2,'sin_catalogar':3}
for a in A:
    idx[a['Id']]=len(nodes); nodes.append([a['Id'],a['Label'],cl[a['clase']],a['nacionalidad'],a['ocupacion'],a['ano_nacimiento'],a['ano_muerte']])
rol={'artista':0,'curador':1,'presentador':2,'apoyo':3}
edges=[[idx[r['Source']],idx[r['Target']],rol[r['rol']]] for r in R]
# proyección dirigida curador/presentador -> artista, por periodo
PER=[[1956,1968],[1969,1982],[1983,1992],[1993,2006],[2007,2016],[2017,2026],[1956,2026]]
year={idx[e['Id']]:(int(e['ano']) if e['ano'] else None) for e in E}
byexpo=collections.defaultdict(lambda:[[],[],[],[]])
for s,t,r in edges: byexpo[s][r].append(t)
comm={};met={}
for a,b in PER:
    G=nx.DiGraph()
    for x,L in byexpo.items():
        y=year[x]
        if y is None or y<a or y>b: continue
        for c in L[1]+L[2]:
            for ar in L[0]:
                if c==ar: continue
                w=G[c][ar]['weight']+1 if G.has_edge(c,ar) else 1
                G.add_edge(c,ar,weight=w)
    U=G.to_undirected()
    cs=nx.community.louvain_communities(U,seed=7,resolution=1.0) if U.number_of_nodes() else []
    cs=sorted(cs,key=len,reverse=True)
    cm={n:i for i,c in enumerate(cs) for n in c}
    bt=nx.betweenness_centrality(G,normalized=False) if G.number_of_nodes()<4000 else {}
    key=f'{a}-{b}'
    comm[key]=[[n,cm[n]] for n in G.nodes()]
    top=sorted(G.nodes(),key=lambda n:-bt.get(n,0))[:15]
    met[key]={'n':G.number_of_nodes(),'e':G.number_of_edges(),'ncom':len(cs),
              'bt':[[n,round(bt.get(n,0),1),G.in_degree(n),G.out_degree(n)] for n in top if bt.get(n,0)>0],
              'out':[[n,G.out_degree(n)] for n in sorted(G.nodes(),key=lambda n:-G.out_degree(n))[:10]]}
    print(key,G.number_of_nodes(),G.number_of_edges(),len(cs),[len(c) for c in cs[:8]])
json.dump({'n':nodes,'e':edges,'per':PER,'comm':comm,'met':met},open('datos_web.json','w'),ensure_ascii=False,separators=(',',':'))
import os;print(os.path.getsize('datos_web.json'))
