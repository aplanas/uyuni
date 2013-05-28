<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://rhn.redhat.com/rhn" prefix="rhn"%>
<%@ taglib uri="http://rhn.redhat.com/tags/list" prefix="rl"%>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean"%>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html"%>
<html:xhtml />

<html>
<body>

 <html:errors />
 <html:messages id="message" message="true">
  <rhn:messages>
   <c:out escapeXml="false" value="${message}" />
  </rhn:messages>
 </html:messages>

 <rhn:toolbar base="h1" img="/img/rhn-icon-info.gif">
  <bean:message key="iss.confirmmasterremove.jsp.toolbar" />
 </rhn:toolbar>

 <p>
 <bean:message key="iss.confirmmasterremove.jsp.areyousure" />
 </p>

 <rhn:dialogmenu mindepth="0" maxdepth="1"
  definition="/WEB-INF/nav/iss_config.xml"
  renderer="com.redhat.rhn.frontend.nav.DialognavRenderer" />
 <c:set var="pageList" value="${requestScope.all}" />

 <h2>
  <bean:message key="iss.confirmmasterremove.jsp.header2" />
 </h2>

 <rl:listset name="issMasterListSet">
  <rhn:csrf />
  <rhn:submitted />
  <rl:list dataset="pageList" name="issMasterList"
   emptykey="iss.slave.jsp.nomasters">
   <rl:column sortable="true" headerkey="iss.master.name" sortattr="label">
    <html:link href="/rhn/admin/iss/MapOrgs.do?mid=${current.id}">
     <c:out value="${current.label}" />
    </html:link>
   </rl:column>
  </rl:list>
  <c:if test="${not empty requestScope.all}">
   <div align="right">
    <rhn:submitted />
    <hr />
    <hr />
    <input type="submit" name="dispatch"
     value='<bean:message key="iss.confirm.remove.masters"/>' />
   </div>
  </c:if>
 </rl:listset>

</body>
</html>
