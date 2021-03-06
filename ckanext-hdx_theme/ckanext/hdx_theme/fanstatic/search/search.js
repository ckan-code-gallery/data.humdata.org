$('document').ready(function(){
    var index = lunr(function () {
        this.field('title', {boost: 10});
        this.field('extra_terms');
        this.field('event', {boost: 1000}); //Little hack to boost the scores of event pages
        this.field('url');
        this.ref('id');

        for(i=0; i<feature_index.length; i++){//This is the part where Lunr is actually not too bright
            feature_index[i]['id'] = i;
            if(feature_index[i]['type'] == 'event'){
                feature_index[i]['event'] = feature_index[i]['title'];
            }else{
                feature_index[i]['event'] = '';
            }
            this.add(feature_index[i])
        }
    });

    var performSearchQuery = function(query) {
      var termList = query.split(' ');
      var modifiedQ = termList.map(term => term.length > 0 ? '+' + term : term).join(' ');
      modifiedQ += modifiedQ.length > 0 ? '*' : '';
      var results = modifiedQ.length > 0 ? index.search(modifiedQ) : [];
      return {
        'q': query,
        'termList': termList,
        'modifiedQ': modifiedQ,
        'results': results
      }
    };


    var searchInfo = performSearchQuery($('#headerSearch').attr('value') || '');
    var results = searchInfo.results;
    if(results.length > 0){//Don't show if we don't have any good matches
        var html = "You might also like:";
        var limit = results.length > 5 ? 5 : results.length;
        for(i=0; i<limit; i++){
            html += ' <a href="'+feature_index[results[i]['ref']]['url']+'">'+feature_index[results[i]['ref']]['title']+'</a> '+feature_index[results[i]['ref']]['type']+' page';
            if(i<limit-1){
                html +=',';
            }
        }
        $('#search-recs').html(html);
    }

    var onSearch = function(){
        var searchInfo = performSearchQuery($(this).val());

        var prevSearch = JSON.parse($("#previous-searches").text());

        // console.log('MODIFIED QUERY IS: ' + searchInfo.modifiedQ);
        var search = searchInfo.results;
        var $results = $(this).parents("form").find('.search-ahead');
        var html = "";
        html += "<ul>";

        if (prevSearch != null && prevSearch.length > 0){
            $(prevSearch).each(function(idx, el){
                html += '<li data-href="'+el.url+'" data-toggle="tooltip" title="'+ el.text +'"><div class="ahead-link"><i class="icon icon-previoussearches"></i>'+process_title(el.text, searchInfo.termList)+'</div><div class="ahead-type">'+el.count+' new results</div></li>';
            });
        }

        if(search.length >0){
            var limit = search.length > 5 ? 5 : search.length;
            for(i=0; i<limit; i++){
                html += '<li data-search-term="'+searchInfo.q+'" data-search-type="'+feature_index[search[i]['ref']]['type']+
                    '" data-href="'+feature_index[search[i]['ref']]['url']+'" ' +
                    'data-toggle="tooltip" title="'+ feature_index[search[i]['ref']]['title'] +'"><div class="ahead-link"><i class="empty"></i>'+
                    process_title(feature_index[search[i]['ref']]['title'], searchInfo.termList)+'</div><div class="ahead-type">'+feature_index[search[i]['ref']]['type']+' page</div></li>';

            }
        }

        html +=
            '<li data-href="/search?q='+ searchInfo.q +'&ext_search_source=main-nav"><div class="ahead-link">' +
            '<i class="icon icon-search"></i>Search <b>'+ searchInfo.q +'</b> in <b>datasets</b>' +
            '</div></li>' +
            '<li data-href="/showcase?q='+ searchInfo.q +'&ext_search_source=main-nav"><div class="ahead-link">' +
            '<i class="icon icon-dataviz"></i>Search <b>'+ searchInfo.q +'</b> in <b>dataviz</b>' +
            '</div></li>';
        html += '</ul>';
        $results.html(html);
        $results.find("li").tooltip({
            placement: 'top',
    	    trigger: 'hover',
            delay: {
                show: 700,
                hide: 100
            }
        });
        $results.show();
    };

    // $('#q, #q2').keyup(onSearch);

    $('#q, #qMobile').keyup(onSearch);
    $('#q, #qMobile').click(onSearch);

    $('.search-ahead').on('mousedown', "li", function(){
        var searchTerm = $(this).attr('data-search-term');
        var resultType = $(this).attr('data-search-type');
        var dataHref = $(this).attr('data-href');
        console.log("Clicked on " + resultType + ". Search term is " + searchTerm);
        var followLink = function () {
            window.location = dataHref;
        };
        if (searchTerm && resultType) {
            hdxUtil.analytics.sendTopBarSearchEvents(searchTerm, resultType).then(followLink, followLink);
        }
        else {
            followLink();
        }
    });

    $('#q, #q2, #qMobile').blur(function(){
        var $results = $(this).parents("form").find('.search-ahead');
        // $results.html('');
        $results.hide();
    });
});

function process_title(title, termList){
  if (termList && termList.length > 0) {
    terms = termList.join('|');
    var re = new RegExp(terms, "gi");
    title = title.replace(re, '<strong>$&</strong>');
  }
  return title;
}
