import os,csv,json,collections,datetime
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
    nodes.append([e['Id'],e['Label'],0,int(e['ano']) if e['ano'] else None,e['fecha_ini'],e['fecha_fin'],e['espacio'],MOD[e['modalidad']],src,1 if (e['pieza_cactus'] or e.get('fuentes_cactus')) else 0,e['tipo_expo'],dias(e['fecha_ini'],e['fecha_fin']),0 if e['confianza'] in ('base_MLT','alta') else 1,1 if e['fuente']=='MLT_DB_07_2016' else 0,(e.get('fuentes_flickr') or '').split(' | ')[0]])
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
comm={};met={};EV={}
ART=set(t for s_,t,r in edges if r==0)
for a,b in PER:
    a,b=a,b
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
    # Louvain depende del orden aleatorio: comunidades de consenso (Lancichinetti y Fortunato 2012).
    # Se corre 50 veces; dos agentes vinculados quedan juntos si caen en la misma comunidad en al menos el 70 % de las ejecuciones.
    cs=[];coh={}
    if U.number_of_nodes():
        runs=[{n:i for i,c in enumerate(nx.community.louvain_communities(U,seed=sd,resolution=1.0)) for n in c} for sd in range(1,51)]
        H=nx.Graph();H.add_nodes_from(U);fr={}
        for u,v in U.edges():
            f=sum(r[u]==r[v] for r in runs)/len(runs);fr[(u,v)]=f
            if f>=.7:H.add_edge(u,v)
        cs=list(nx.connected_components(H))
    cs=sorted(cs,key=len,reverse=True)
    cm={n:i for i,c in enumerate(cs) for n in c}
    if U.number_of_nodes():
        acc=collections.defaultdict(list)
        for (u,v),f in fr.items():
            if cm[u]==cm[v]: acc[cm[u]].append(f)
        coh={k:round(sum(v)/len(v),2) for k,v in acc.items()}
    bt=nx.betweenness_centrality(G,normalized=False) if G.number_of_nodes()<4000 else {}
    # vector propio (no dirigido, ponderado, componente gigante; fuera de ella vale 0)
    ev={}
    if U.number_of_nodes():
        Uw=nx.Graph()
        for u,v,d in G.edges(data=True):
            w=d['weight']+(Uw[u][v]['weight'] if Uw.has_edge(u,v) else 0);Uw.add_edge(u,v,weight=w)
        gc=Uw.subgraph(max(nx.connected_components(Uw),key=len))
        if gc.number_of_nodes()>2: ev=nx.eigenvector_centrality_numpy(gc,weight='weight')
    EV[(a,b)]=(ev,dict(G.to_undirected().degree()),set(n for x,L in byexpo.items() if year[x] and a<=year[x]<=b for n in L[1]+L[2]))
    key=f'{a}-{b}'
    comm[key]=[[n,cm[n]] for n in G.nodes()]
    top=sorted(G.nodes(),key=lambda n:-bt.get(n,0))[:15]
    met[key]={'n':G.number_of_nodes(),'e':G.number_of_edges(),'ncom':len(cs),
              'bt':[[n,round(bt.get(n,0),1),G.in_degree(n),G.out_degree(n)] for n in top if bt.get(n,0)>0],
              'out':[[n,G.out_degree(n)] for n in sorted(G.nodes(),key=lambda n:-G.out_degree(n))[:10]],
              'ev':[[n,round(ev[n],3)] for n in sorted(ev,key=lambda n:-ev[n])[:15]],
              'evall':[[n,round(v,4)] for n,v in ev.items() if v>=0.0005]}
    cur=EV[(a,b)][2];ca=[ev.get(n,0) for n in cur if n in G and n in ART];co=[ev.get(n,0) for n in cur if n in G and n not in ART]
    met[key]['evrol']=[len(ca),round(sum(ca)/len(ca),4) if ca else None,len(co),round(sum(co)/len(co),4) if co else None]
    print(key,G.number_of_nodes(),G.number_of_edges(),len(cs),[len(c) for c in cs[:8]])
from scipy.stats import spearmanr
# cohesión de las comunidades de 1956-2026 (última iteración): promedio de la fracción de ejecuciones en que sus vínculos internos quedan juntos
stab=[[k,v,len(cs[k])] for k,v in sorted(coh.items()) if len(cs[k])>=20]
print('estabilidad',stab)
pred=[]
for i in range(len(PER)-2):
    (ev,dg,_),(ev2,dg2,_)=EV[tuple(PER[i])],EV[tuple(PER[i+1])]
    ns=list(dg);nxt=[dg2.get(n,0) for n in ns]
    pred.append([PER[i],PER[i+1],round(spearmanr([ev.get(n,0) for n in ns],nxt).correlation,2),round(spearmanr([dg[n] for n in ns],nxt).correlation,2),len(ns),sum(1 for v in nxt if v)])
print(pred)
# programas de mano (PDF) y piezas gráficas (imagen) por exposición: [id, páginas, MB, tipo, 'pdf'|'img']
prog={}
W='/home/claude/mlt-web/'
if os.path.exists(W+'data/programas.csv'):
    for r in csv.DictReader(open(W+'data/programas.csv',encoding='utf-8')):
        if r['id_expo'] in idx: prog.setdefault(r['id_expo'],[]).append([r['id_programa'],int(r['paginas']),float(r['mb']),r['tipo'],'pdf'])
if os.path.exists(W+'data/piezas_fuentes.csv'):
    for r in csv.DictReader(open(W+'data/piezas_fuentes.csv',encoding='utf-8')):
        i=r['id_expo'].replace('.','')
        if r['id_expo'] in idx: prog.setdefault(r['id_expo'],[]).append([i,1,round(os.path.getsize(W+'programas/piezas/'+i+'.jpg')/1e6,1),r['tipo'],'img'])
json.dump({'n':nodes,'e':edges,'per':PER,'comm':comm,'met':met,'pred':pred,'prog':prog,'stab':stab},open('datos_web.json','w'),ensure_ascii=False,separators=(',',':'))
import os;print(os.path.getsize('datos_web.json'))
