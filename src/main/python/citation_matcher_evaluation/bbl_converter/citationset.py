import codecs

_last_article_id = 10000

class CitationSet(object):
    def __init__(self):
        global _last_article_id
        self.set = []
        _last_article_id += 1
        self.articleId = _last_article_id
    
    def add(self, key, value):
        self.set.append((key, value))

    def write_txt(self, filename):
        with codecs.open(filename, 'w', encoding="utf8") as file:
            for (k, v) in self.set:
                file.write(v + '\n')
    
    def write_nlm(self, filename):
        with codecs.open(filename, 'w', encoding="utf8") as file:
            file.write(
                       """
<article>
<front>
<journal-meta>
         <journal-id journal-id-type="uri">http://www.mat.ucm.es/serv/revista/</journal-id>
         <journal-title-group>
            <journal-title>Revista Matem&#225;tica de la Universidad Complutense de Madrid</journal-title></journal-title-group>
         <issn>0214-3577</issn></journal-meta>
      <article-meta>
         <article-id pub-id-type="dmle-id">""" + str(self.articleId) + """</article-id>
         <title-group>
            <article-title xml:lang="en">Orthonormal bases for spaces of continuous and continuously differentiable functions defined on a subset of Zp.</article-title>
            <trans-title-group xml:lang="es">
               <trans-title>Bases ortonormales para espacios de funciones continuas y cont&#237;nuamente diferenciables definidas en un subconjunto de Zp.</trans-title></trans-title-group></title-group>
         <contrib-group>
            <contrib contrib-type="author">
               <name>
                  <surname>Verdoodt</surname>
                  <given-names>Ann</given-names></name>
               <xref ref-type="aff" rid="AFF1">1</xref></contrib></contrib-group>
         <aff id="AFF1">
            <label>1</label>
            <institution>Fac. Appl. Sci. Vrije Univ., Bruselas, B&#233;lgica</institution></aff>
         <pub-date>
            <year>1996</year></pub-date>
         <volume>9</volume>
         <issue>2</issue>
         <fpage>295</fpage>
         <lpage>307</lpage>
         <ext-link ext-link-type="mr-item-id" ns1:href="http://www.ams.org/mathscinet-getitem?mr=MR1430780" xmlns:ns1="http://www.w3.org/1999/xlink">MR1430780</ext-link>
         <ext-link ext-link-type="zbl-item-id" ns1:href="http://www.zentralblatt-math.org/zmath/en/search/?q=an:0882.46033" xmlns:ns1="http://www.w3.org/1999/xlink">0882.46033</ext-link>
         <self-uri ns1:href="http://dmle.cindoc.csic.es/revistas/detalle.php?numero=707" xmlns:ns1="http://www.w3.org/1999/xlink">Access to full text</self-uri>
         <abstract xml:lang="en">
            <p>Let K be a non-Archimedean valued field which contains Qp, and suppose that K is complete for the valuation |&#183;|, which extends the p-adic valuation. Vq is the closure of the set {aqn | n = 0,1,2,...} where a and q are two units of Zp, q not a root of unity. C(Vq --&amp;gt; K) (resp. C1(Vq --&amp;gt; K)) is the Banach space of continuous functions (resp. continuously differentiable functions) from Vq to K. Our aim is to find orthonormal bases for C(Vq --&amp;gt; K) and C1(Vq --&amp;gt; K).</p></abstract>
         <kwd-group xml:lang="es">
            <kwd>Bases ortonormales</kwd>
            <kwd>Algebra de Banach no arquimediana</kwd>
            <kwd>Enteros p-&#225;dicos</kwd>
            <kwd>Espacios de funciones diferenciables</kwd>
            <kwd>An&#225;lisis funcional</kwd>
            <kwd>Funciones continuas</kwd></kwd-group>
         <kwd-group kwd-group-type="unesco" xml:lang="es">
            <compound-kwd>
               <compound-kwd-part content-type="code">120203</compound-kwd-part>
               <compound-kwd-part content-type="expansion">Algebras y espacios Banach</compound-kwd-part></compound-kwd></kwd-group>
         <custom-meta-group>
            <custom-meta>
               <meta-name>provider</meta-name>
               <meta-value>dmle</meta-value></custom-meta></custom-meta-group></article-meta></front>
<body/>
<back>
<ref-list>
""")
            for (k, v) in self.set:
                file.write('<ref id="%s"><label>%s</label><mixed-citation publication-type="none">\n' % (k, k))
                file.write(v)
                file.write('</mixed-citation></ref>\n')
            
            file.write(
                       """
</ref-list>
</back>
</article>
""")

    def write_mapfile(self, filename):
        with codecs.open(filename, 'w', encoding="utf8") as file:
            for (k, v) in self.set:
                file.write(k + '\n')



